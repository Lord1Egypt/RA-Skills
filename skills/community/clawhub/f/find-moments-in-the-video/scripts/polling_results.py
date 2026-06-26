import argparse
import json
import time
import os
import sys
import subprocess
import urllib.request
import urllib.error
import socket
from datetime import datetime, timedelta

# Get API Key from environment variable
API_KEY = os.environ.get("WAYIN_API_KEY")

if not API_KEY:
    print("Error: WAYIN_API_KEY environment variable is not set.", file=sys.stderr)
    sys.exit(1)

BASE_URL = "https://wayinvideo-api.wayin.ai/api/v2/clips/find-moments"
HEADERS = {
    "Content-Type": "application/json",
    "Authorization": f"Bearer {API_KEY}",
    "x-wayinvideo-api-version": "v2",
    "user-agent": "find-moments skill"
}

def get_result(project_id, save_file, sleep_interval=15, max_timeout_seconds=14400, event_interval=300):
    url = f"{BASE_URL}/results/{project_id}"
    start_time = time.time()
    last_reminder_time = time.time()
    last_result_count = 0
    last_update_time = time.time()
    has_updated_ongoing = False

    while True:
        try:
            req = urllib.request.Request(url, headers=HEADERS, method="GET")
            with urllib.request.urlopen(req, timeout=30) as response:
                response_text = response.read().decode("utf-8")

                data_res = json.loads(response_text).get("data", {})
                status = data_res.get("status")
                current_moments = data_res.get("clips", [])
                current_count = len(current_moments)

                # Update save file if status is SUCCEEDED, FAILED or ONGOING with new results
                # Also update once when status first becomes ONGOING even if no results yet
                should_update = (status in ["SUCCEEDED", "FAILED"]) or \
                               (status == "ONGOING" and current_count > last_result_count) or \
                               (status == "ONGOING" and not has_updated_ongoing)

                if should_update:
                    msg = None
                    try:
                        abs_path = update_save_file(save_file, project_id, data_res, status=status)
                        
                        if event_interval > 0:
                            if status == "SUCCEEDED":
                                msg = f"✅ WayinVideo [Find Moments] task {project_id} SUCCEEDED! Total moments: {current_count}. View at {abs_path}"
                            elif status == "FAILED":
                                msg = f"❌ WayinVideo [Find Moments] task {project_id} FAILED. View details at {abs_path}"
                            elif status == "ONGOING" and current_count > last_result_count:
                                new_count = current_count - last_result_count
                                msg = f"🔔 WayinVideo [Find Moments] task {project_id} has {new_count} new results (Total: {current_count}). View at {abs_path}"
                            elif status == "ONGOING" and not has_updated_ongoing:
                                msg = f"🔄 WayinVideo [Find Moments] task {project_id} is now ONGOING. View at {abs_path}"
                            
                            if msg:
                                send_system_event(msg)
                                last_reminder_time = time.time()

                        if status == "ONGOING":
                            has_updated_ongoing = True

                        last_result_count = current_count
                        last_update_time = time.time()
                    except Exception as e:
                        print(f"DEBUG: Failed to update save file: {e}", file=sys.stderr)

                if status == "SUCCEEDED":
                    return data_res, None
                elif status == "FAILED":
                    return None, f"WayinVideo task failed. Raw response: {json.dumps(data_res)}"
                
                print(f"Status: {status}... (Moments: {current_count}) waiting {sleep_interval}s", file=sys.stderr)

                current_time = time.time()
                if current_time - start_time > max_timeout_seconds:
                    timeout_msg = (
                        f"Timeout: Task {project_id} did not finish within {max_timeout_seconds} seconds. "
                        f"The task is likely still processing on the server."
                    )
                    return None, timeout_msg
                
                # Send "still running" reminder only if no updates in the last event_interval
                if event_interval > 0 and (current_time - last_reminder_time >= event_interval) and (current_time - last_update_time >= event_interval):
                    reminder_text = f"Reminder: WayinVideo [Find Moments] task {project_id} is still running (Status: {status})."
                    send_system_event(reminder_text)
                    last_reminder_time = current_time
        except urllib.error.HTTPError as e:
            print(f"DEBUG: HTTP error during polling: status {e.code}", file=sys.stderr)
            if e.code in (401, 403, 404):
                return False, f"Fatal HTTP Error {e.code}. Stopping."
        except (urllib.error.URLError, TimeoutError, socket.timeout) as e:
            # Catch network timeouts and keep polling
            print(f"DEBUG: Network timeout or connection error: {str(e)}. Retrying in {sleep_interval}s...", file=sys.stderr)
        except Exception as e:
            print(f"DEBUG: Error during polling: {str(e)}", file=sys.stderr)
            return None, f"Error during polling: {str(e)}"

        time.sleep(sleep_interval)

def send_system_event(text):
    try:
        subprocess.run([
            "openclaw", "system", "event",
            "--text", text,
            "--mode", "now"
        ], check=True, capture_output=True, text=True)
        print(f"DEBUG: Sent system event: {text}", file=sys.stderr)
    except Exception as e:
        print(f"DEBUG: Failed to send system event: {e}", file=sys.stderr)

def update_save_file(file_path, project_id, api_response, status=None, error=None):
    with open(file_path, "r", encoding="utf-8") as f:
        data = json.load(f)
    
    # Validate project ID
    existing_id = data.get("_metadata", {}).get("id")
    if str(existing_id) != str(project_id):
        raise ValueError(f"Project ID mismatch: Expected {existing_id}, but got {project_id}.")

    now = datetime.now()
    data["_metadata"]["updated_at"] = now.isoformat()
    
    if api_response:
        data["api_response"] = api_response
        data["_metadata"]["status"] = status or api_response.get("status")

        # Add project name if available in response
        if "name" in api_response:
            data["_metadata"]["name"] = api_response["name"]
        
        if status == "SUCCEEDED":
            data["_metadata"]["task_finished_at"] = now.isoformat()
            data["_metadata"]["task_expires_at"] = (now + timedelta(days=3)).isoformat()
            
            moments = api_response.get("clips", [])
            if moments and any(moment.get("export_link") for moment in moments):
                data["_metadata"]["export_links_expire_at"] = (now + timedelta(hours=24)).isoformat()
            
    if error:
        data["error"] = error
        if "Timeout" in error:
            data["_metadata"]["status"] = "TIMEOUT"
        else:
            data["_metadata"]["status"] = "FAILED"

    with open(file_path, "w", encoding="utf-8") as f:
        json.dump(data, f, ensure_ascii=False, indent=2)
    
    return os.path.abspath(file_path)

def main():
    parser = argparse.ArgumentParser()
    parser.add_argument("--project-id", required=True)
    parser.add_argument("--save-file", required=True)
    parser.add_argument("--event-interval", type=int, default=0, help="Interval (seconds) for status/update events. 0 to disable.")
    args = parser.parse_args()

    try:
        update_save_file(args.save_file, args.project_id, None)
    except Exception as e:
        print(f"ERROR: Initial file check failed: {e}", file=sys.stderr)
        sys.exit(1)

    try:
        result, error = get_result(args.project_id, args.save_file, event_interval=args.event_interval)
        abs_path = update_save_file(args.save_file, args.project_id, result, error=error)
        
        if error:
            print(f"ERROR: {error}. Result saved to {abs_path}")
            sys.exit(1)
        else:
            print(f"SUCCESS: Raw API result updated at {abs_path}")
    except Exception as e:
        print(f"ERROR: {str(e)}", file=sys.stderr)
        sys.exit(1)

if __name__ == "__main__":
    main()
