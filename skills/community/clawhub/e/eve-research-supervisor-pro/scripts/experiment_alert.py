#!/usr/bin/env python3
"""
experiment_alert.py — Feature 10: Real-Time Experiment Alerts
Monitors your running experiments and alerts you when:
  - Training finishes (success or failure)
  - A metric milestone is hit (e.g. BER < 0.1)
  - Job crashes or runs out of memory
  - Results are ready to pull

Usage:
  python3 experiment_alert.py watch  <job_id> [--metric BER --threshold 0.1]
  python3 experiment_alert.py poll   <job_id> [--interval 60]
  python3 experiment_alert.py parse  <log_file>           — extract metrics from log
  python3 experiment_alert.py update <project> <log_file> — auto-update data template
"""

import sys
import os
import re
import json
import time
import datetime
import subprocess

BASE       = os.path.expanduser("~/.openclaw/workspace/research-supervisor-pro")
CONFIG     = os.path.join(BASE, "memory/server_config.json")
ALERTS_LOG = os.path.join(BASE, "memory/alerts.log")


def load_server_config():
    if not os.path.exists(CONFIG):
        return {}
    with open(CONFIG) as f:
        return json.load(f)


def log_alert(message):
    os.makedirs(os.path.dirname(ALERTS_LOG), exist_ok=True)
    ts = datetime.datetime.now().strftime("%Y-%m-%d %H:%M:%S")
    with open(ALERTS_LOG, "a") as f:
        f.write(f"[{ts}] {message}\n")
    print(f"🔔 ALERT [{ts}]: {message}")


def ssh_run(cmd, timeout=30):
    cfg = load_server_config()
    host = cfg.get("host", "")
    user = cfg.get("user", "")
    port = cfg.get("port", 22)
    key  = cfg.get("ssh_key", "")
    if not host:
        return None
    ssh = ["ssh", "-o", "StrictHostKeyChecking=no", "-o", f"ConnectTimeout={timeout}",
           "-p", str(port)]
    if key:
        ssh += ["-i", os.path.expanduser(key)]
    ssh += [f"{user}@{host}", cmd]
    try:
        r = subprocess.run(ssh, capture_output=True, text=True, timeout=timeout+5)
        return r.stdout.strip()
    except Exception:
        return None


# ── Metric Patterns ───────────────────────────────────────────────────────────
METRIC_PATTERNS = {
    "BER":          r"(?:BER|bit.error.rate)[:\s=]+([0-9]+\.?[0-9]*)",
    "BitAcc":       r"(?:bit.?acc(?:uracy)?|BA)[:\s=]+([0-9]+\.?[0-9]*)",
    "PSNR":         r"PSNR[:\s=]+([0-9]+\.?[0-9]*)",
    "SSIM":         r"SSIM[:\s=]+([0-9]+\.?[0-9]*)",
    "Loss":         r"(?:loss|train.loss)[:\s=]+([0-9]+\.?[0-9]*)",
    "Epoch":        r"[Ee]poch[:\s]+([0-9]+)",
    "Accuracy":     r"(?:acc(?:uracy)?)[:\s=]+([0-9]+\.?[0-9]*)",
    "DetectionAcc": r"(?:detection.?acc(?:uracy)?)[:\s=]+([0-9]+\.?[0-9]*)",
}

FINISH_PATTERNS = [
    r"training complete",
    r"finished training",
    r"job complete",
    r"saved model",
    r"best model saved",
    r"evaluation complete",
    r"done\.",
]

ERROR_PATTERNS = [
    r"error|exception|traceback",
    r"cuda out of memory",
    r"killed",
    r"nan loss",
    r"inf loss",
    r"segmentation fault",
]


def parse_log(log_text):
    """Extract all metrics from a log file text."""
    metrics_found = {}
    lines = log_text.split("\n")

    for line in lines:
        line_lower = line.lower()

        # Check metrics
        for name, pattern in METRIC_PATTERNS.items():
            m = re.search(pattern, line, re.IGNORECASE)
            if m:
                try:
                    val = float(m.group(1))
                    if name not in metrics_found:
                        metrics_found[name] = []
                    metrics_found[name].append(val)
                except ValueError:
                    pass

        # Check finish
        for fp in FINISH_PATTERNS:
            if re.search(fp, line_lower):
                metrics_found["__finished__"] = True

        # Check errors
        for ep in ERROR_PATTERNS:
            if re.search(ep, line_lower):
                if "__errors__" not in metrics_found:
                    metrics_found["__errors__"] = []
                metrics_found["__errors__"].append(line.strip()[:100])

    return metrics_found


def print_metrics_summary(metrics):
    print("\n📊 EXTRACTED METRICS:")
    print("━" * 50)
    for name, values in metrics.items():
        if name.startswith("__"):
            continue
        if isinstance(values, list) and values:
            print(f"  {name:<15}: last={values[-1]:.4f}  min={min(values):.4f}  max={max(values):.4f}  ({len(values)} readings)")
    if metrics.get("__finished__"):
        print("  ✅ Training COMPLETED")
    errors = metrics.get("__errors__", [])
    if errors:
        print(f"  ❌ {len(errors)} errors found:")
        for e in errors[:3]:
            print(f"     {e}")
    print("━" * 50)


def update_data_template(project, metrics):
    """Auto-update experiment_data_template.json with extracted metrics."""
    template_path = os.path.join(BASE, "research", project, "experiment_data.json")

    existing = {}
    if os.path.exists(template_path):
        with open(template_path) as f:
            existing = json.load(f)

    # Build training curve if epochs + metric present
    if "Epoch" in metrics and ("BER" in metrics or "Loss" in metrics):
        epochs = metrics.get("Epoch", [])
        bers = metrics.get("BER", [])
        losses = metrics.get("Loss", [])

        if "experiments" not in existing:
            existing["experiments"] = []

        if bers and len(bers) == len(epochs):
            existing["experiments"].append({
                "name": "BER vs Epochs",
                "xlabel": "Epoch",
                "ylabel": "BER",
                "label": "Bit Error Rate during training",
                "x": epochs[:len(bers)],
                "y": bers
            })
        if losses:
            existing["experiments"].append({
                "name": "Training Loss",
                "xlabel": "Epoch",
                "ylabel": "Loss",
                "label": "Training loss curve",
                "x": list(range(len(losses))),
                "y": losses
            })

    os.makedirs(os.path.dirname(template_path), exist_ok=True)
    with open(template_path, "w") as f:
        json.dump(existing, f, indent=2)

    print(f"✅ experiment_data.json updated → {template_path}")
    return template_path


def poll_job(job_id, interval=60, metric=None, threshold=None, project=None):
    """Poll job status every N seconds, alert on completion or milestone."""
    cfg = load_server_config()
    workdir = cfg.get("workdir", "~")

    print(f"🔍 Polling job {job_id} every {interval}s...")
    if metric and threshold:
        print(f"   Alert when {metric} {'<' if float(threshold) < 0.5 else '>'} {threshold}")
    print("   (Ctrl+C to stop)\n")

    alerted_milestone = False
    last_line_count = 0

    while True:
        try:
            # Check if job still running
            status = ssh_run(f"squeue -j {job_id} --noheader 2>/dev/null")

            # Get latest log lines
            log_content = ssh_run(f"find {workdir} -name '*{job_id}*' -newer /tmp -exec tail -100 {{}} \\; 2>/dev/null | tail -200")

            if log_content:
                metrics = parse_log(log_content)

                # Check milestone
                if metric and threshold and not alerted_milestone:
                    vals = metrics.get(metric, [])
                    if vals:
                        last_val = vals[-1]
                        thr = float(threshold)
                        if (thr < 0.5 and last_val < thr) or (thr >= 0.5 and last_val > thr):
                            log_alert(f"🎯 MILESTONE: Job {job_id} — {metric}={last_val:.4f} (threshold={threshold})")
                            alerted_milestone = True

                # Check completion
                if metrics.get("__finished__"):
                    log_alert(f"✅ Job {job_id} COMPLETED!")
                    print_metrics_summary(metrics)
                    if project:
                        update_data_template(project, metrics)
                    break

                # Check errors
                errors = metrics.get("__errors__", [])
                if errors:
                    log_alert(f"❌ Job {job_id} has errors: {errors[0]}")

                # Show current status
                epoch_vals = metrics.get("Epoch", [])
                ber_vals   = metrics.get("BER", [])
                ts = datetime.datetime.now().strftime("%H:%M:%S")
                status_line = f"[{ts}] Job {job_id}"
                if epoch_vals:
                    status_line += f" | Epoch {int(epoch_vals[-1])}"
                if ber_vals:
                    status_line += f" | BER {ber_vals[-1]:.4f}"
                print(status_line, end="\r")

            if not status:
                log_alert(f"✅ Job {job_id} no longer in queue — likely finished")
                break

            time.sleep(interval)

        except KeyboardInterrupt:
            print("\n\nStopped polling.")
            break


def parse_local_log(log_file):
    """Parse a local log file and extract metrics."""
    if not os.path.exists(log_file):
        print(f"❌ File not found: {log_file}")
        return
    with open(log_file) as f:
        content = f.read()
    metrics = parse_log(content)
    print_metrics_summary(metrics)
    return metrics


if __name__ == "__main__":
    if len(sys.argv) < 2:
        print(__doc__)
        sys.exit(1)

    action = sys.argv[1]

    if action == "watch" and len(sys.argv) >= 3:
        job_id    = sys.argv[2]
        metric    = None
        threshold = None
        project   = None
        for i, arg in enumerate(sys.argv):
            if arg == "--metric"    and i+1 < len(sys.argv): metric    = sys.argv[i+1]
            if arg == "--threshold" and i+1 < len(sys.argv): threshold = sys.argv[i+1]
            if arg == "--project"   and i+1 < len(sys.argv): project   = sys.argv[i+1]
        poll_job(job_id, interval=30, metric=metric, threshold=threshold, project=project)

    elif action == "poll" and len(sys.argv) >= 3:
        job_id   = sys.argv[2]
        interval = int(sys.argv[4]) if "--interval" in sys.argv else 60
        poll_job(job_id, interval=interval)

    elif action == "parse" and len(sys.argv) >= 3:
        parse_local_log(sys.argv[2])

    elif action == "update" and len(sys.argv) >= 4:
        metrics = parse_local_log(sys.argv[3])
        if metrics:
            update_data_template(sys.argv[2], metrics)

    else:
        print(__doc__)
