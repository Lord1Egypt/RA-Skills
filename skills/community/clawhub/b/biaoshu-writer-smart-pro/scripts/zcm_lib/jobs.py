"""Job polling, result download, and progress streaming helpers."""
import json
import os
import sys
import time
import urllib.error
import urllib.request


def poll_job(job_id, *, interval=5, timeout=3600, request_json_fn,
             format_progress_line_fn, log_fn, die_fn,
             error_hints, guide_insufficient_balance_fn):
    """Poll a job until terminal state and return the final status payload."""
    deadline = time.time() + timeout
    last = ""
    while True:
        status_payload = request_json_fn("GET", f"/jobs/{job_id}")
        status = status_payload.get("status")
        progress = status_payload.get("progress") or {}
        line = format_progress_line_fn(progress, status=status, include_job_id=job_id)
        if line != last:
            log_fn(line)
            last = line
        if status == "succeeded":
            return status_payload
        if status in ("failed", "canceled"):
            error = status_payload.get("error") or {}
            error_code = error.get("code", "")
            if error_code in ("insufficient_balance", "insufficient_points"):
                error = dict(error, task_failed=True, terminal_status=status, job_id=job_id)
                guide_insufficient_balance_fn(error)
            hint = error_hints.get(error_code, "")
            extra = "（服务重启导致，需重新提交）" if error_code == "worker_lost" else ""
            die_fn(f"任务 {status}：{error_code} {error.get('message','')} {hint}{extra}".strip(), code=1)
        if time.time() > deadline:
            die_fn(f"轮询超时（>{timeout}s），任务仍未完成。可稍后用 `job {job_id}` 继续查看。", code=1)
        time.sleep(interval)


def cmd_job(args, *, request_json_fn):
    data = request_json_fn("GET", f"/jobs/{args.job_id}")
    print(json.dumps(data, ensure_ascii=False, indent=2))


def download_result(job_id, out_path, *, base_url_fn, headers_fn,
                    handle_http_error_fn, die_fn):
    """Stream a generated .docx result to disk."""
    url = base_url_fn() + f"/jobs/{job_id}/result"
    req = urllib.request.Request(url, headers=headers_fn(), method="GET")
    try:
        with urllib.request.urlopen(req) as resp, open(out_path, "wb") as handle:
            while True:
                chunk = resp.read(65536)
                if not chunk:
                    break
                handle.write(chunk)
    except urllib.error.HTTPError as exc:
        handle_http_error_fn(exc)
    except urllib.error.URLError as exc:
        die_fn(f"网络错误：{exc.reason}", code=1)


def get_download_url(job_id, *, request_json_fn):
    return request_json_fn("GET", f"/jobs/{job_id}/download-url")


def print_download_link(job_id, *, request_json_fn, format_seconds_fn,
                        format_bytes_fn, log_fn):
    data = get_download_url(job_id, request_json_fn=request_json_fn)
    filename = data.get("filename") or f"bid_{job_id}.docx"
    url = data.get("download_url") or ""
    expires = format_seconds_fn(data.get("expires_in")) or "短时间"
    size = format_bytes_fn(data.get("size_bytes"))
    partial = bool(data.get("partial"))
    completion = data.get("completion") if isinstance(data.get("completion"), dict) else {}
    outline_id = data.get("outline_id")
    log_fn(f"成品标书已生成：{filename}")
    if partial:
        generated = completion.get("generated")
        total = completion.get("total")
        missing = completion.get("missing")
        if total:
            log_fn(f"注意：当前是半成品标书，正文已生成 {generated}/{total} 节，尚缺 {missing} 节；可先下载使用。")
        else:
            log_fn("注意：当前是半成品标书；可先下载使用。")
        if data.get("continue_available") and outline_id:
            log_fn(f"补足可用字数后，可继续执行：continue-generate <project_id> --outline-id {outline_id} --no-wait")
    log_fn(f"文件大小：{size}；下载链接 {expires} 内有效。")
    log_fn("如需保存到本地，请告诉我保存路径，我来下载；若链接失效，我可重新获取新的下载链接。")
    print(url)


def cmd_result(args, *, request_json_fn, download_result_fn,
               platform_reminder_fn, zh_risk_fn, log_fn):
    if args.output:
        download_result_fn(args.job_id, args.output)
        log_fn(f"已保存：{args.output}")
        print(args.output)
        platform_reminder_fn()
        return
    try:
        data = request_json_fn("GET", f"/jobs/{args.job_id}/result")
    except (UnicodeDecodeError, json.JSONDecodeError):
        print(
            "结果不是 JSON，可能是成品标书文件。请使用 download-url 获取下载链接，"
            "或使用 result <job_id> -o <保存路径.docx> 直接保存。",
            file=sys.stderr,
            flush=True,
        )
        raise SystemExit(1)
    print(json.dumps(zh_risk_fn(data), ensure_ascii=False, indent=2))


def cmd_download_url(args, *, print_download_link_fn):
    print_download_link_fn(args.job_id)


def cmd_cancel(args, *, request_json_fn):
    data = request_json_fn("POST", f"/jobs/{args.job_id}/cancel")
    print(json.dumps(data, ensure_ascii=False, indent=2))


def progress_stream(args, *, request_json_fn, format_progress_line_fn,
                    guide_insufficient_balance_fn, error_hints):
    """Stream progress lines to stdout for agent-side monitors."""
    print(f"进度更新：已开始监听任务进度 job_id={args.job_id}。我会继续后台监听。", flush=True)
    deadline = time.time() + args.timeout
    last = ""
    last_pct = None
    last_stage = ""
    last_emit_at = 0.0
    last_retry_at = 0.0
    while True:
        try:
            status_payload = request_json_fn("GET", f"/jobs/{args.job_id}")
        except (Exception, SystemExit):
            now = time.time()
            if last_retry_at <= 0 or (now - last_retry_at) >= args.heartbeat:
                print("[重试中] 正在重新获取任务进度，网络或平台短暂波动时会自动继续", flush=True)
                last_retry_at = now
            time.sleep(1)
            continue
        status = status_payload.get("status")
        progress = status_payload.get("progress") or {}
        if status in ("queued", "running") and not progress:
            now = time.time()
            line = (
                "进度更新：任务已开始运行，正在等待平台返回生成阶段进度。我会继续后台监听。"
                if status == "running"
                else "进度更新：任务已提交，正在排队等待平台开始处理。我会继续后台监听。"
            )
            heartbeat_due = last_emit_at <= 0 or (now - last_emit_at) >= args.heartbeat
            if heartbeat_due:
                print(line, flush=True)
                last = line
                last_emit_at = now
            if time.time() > deadline:
                print(f"[超时] 任务超过 {args.timeout}s 未完成", flush=True)
                sys.exit(1)
            time.sleep(args.interval)
            continue
        pct = progress.get("percent")
        stage_key = "|".join(str(progress.get(key) or "") for key in (
            "stage", "stage_label", "message", "current_step", "total_steps", "current_step_label",
        )) + f"|{status}"
        stage_changed = stage_key != last_stage
        pct_stepped = (
            last_pct is None or pct is None or abs(pct - last_pct) >= args.step or stage_changed
        )
        heartbeat_due = last_emit_at <= 0 or (time.time() - last_emit_at) >= args.heartbeat
        line = format_progress_line_fn(progress, status=status)
        if (line != last and pct_stepped) or heartbeat_due:
            print(line, flush=True)
            last = line
            last_stage = stage_key
            last_emit_at = time.time()
            if pct is not None:
                last_pct = pct
        if status == "succeeded":
            print("[完成]", flush=True)
            return
        if status in ("failed", "canceled"):
            error = status_payload.get("error") or {}
            error_code = error.get("code", "")
            if error_code in ("insufficient_balance", "insufficient_points"):
                error = dict(error, task_failed=True, terminal_status=status, job_id=args.job_id)
                print("[失败] 本次任务已停止；平台不会自动续跑。若平台已导出半成品，可用 download-url 获取；补足可用字数后可继续生成正文。", flush=True)
                guide_insufficient_balance_fn(error)
            hint = error_hints.get(error_code, "")
            print(f"[失败] {error_code} {error.get('message', '')} {hint}".strip(), flush=True)
            sys.exit(1)
        if time.time() > deadline:
            print(f"[超时] 任务超过 {args.timeout}s 未完成", flush=True)
            sys.exit(1)
        time.sleep(args.interval)
