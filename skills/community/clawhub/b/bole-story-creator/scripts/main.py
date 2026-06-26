import json
import os
import time
import urllib.request
from datetime import datetime
import uuid
import sys


def generate_uuid() -> str:
    return str(uuid.uuid4())


def create_access_token() -> str:
    url = "https://bole.bonanai.com/api/auth/loginByAccessKey"
    headers = {
        "Content-Type": "application/json;charset=UTF-8",
    }
    payload = {
        "accessKey": os.environ.get("BOLE_ACCESS_KEY"),
    }

    data = json.dumps(payload).encode("utf-8")
    req = urllib.request.Request(url=url, data=data, headers=headers, method="POST")

    with urllib.request.urlopen(req) as resp:
        resp_body = resp.read().decode("utf-8")

    resp_json = json.loads(resp_body)
    access_token = resp_json.get("data", {}).get("access_token")
    print(f"access_token: {access_token}", file=sys.stderr)
    return access_token


def create_episode(token: str, project_id: str) -> str:
    url = "https://bole.bonanai.com/api/bkk/episode"

    headers = {
        "Authorization": f"Bearer {token}",
        "ClientID": "e5cd7e4891bf95d1d19206ce24a7b32e",
        "Accept": "application/json, text/plain, */*",
        "Content-Type": "application/json;charset=UTF-8",
    }

    payload = {
        "projectId": project_id,
        "name": datetime.now().strftime("%Y-%m-%d %H:%M:%S:%f")[:-3],
        "index": 2,
    }

    data = json.dumps(payload).encode("utf-8")
    req = urllib.request.Request(url=url, data=data, headers=headers, method="POST")

    with urllib.request.urlopen(req) as resp:
        resp_body = resp.read().decode("utf-8")

    resp_json = json.loads(resp_body)
    episode_id = resp_json.get("data")
    print(f"episodeId: {episode_id}", file=sys.stderr)
    return episode_id


def create_workspace(token: str, project_id: str, episode_id: str) -> str:
    url = "https://bole.bonanai.com/api/bkk/project/workspace/empty"

    headers = {
        "Authorization": f"Bearer {token}",
        "ClientID": "e5cd7e4891bf95d1d19206ce24a7b32e",
        "Accept": "application/json, text/plain, */*",
        "Content-Type": "application/json;charset=UTF-8",
    }

    payload = {
        "projectId": project_id,
        "episodeId": episode_id,
    }

    data = json.dumps(payload).encode("utf-8")
    req = urllib.request.Request(url=url, data=data, headers=headers, method="POST")

    with urllib.request.urlopen(req) as resp:
        resp_body = resp.read().decode("utf-8")

    resp_json = json.loads(resp_body)
    workspace_id = resp_json.get("data", {}).get("id")
    print(f"workspaceId: {workspace_id}", file=sys.stderr)
    return workspace_id


def create_storyboard(
    token: str,
    project_id: str,
    episode_id: str,
    workspace_id: str,
    text: str,
) -> None:
    url = "https://bole.bonanai.com/api/bkk/ai/chatStoryGenerate"

    headers = {
        "Authorization": f"Bearer {token}",
        "ClientID": "e5cd7e4891bf95d1d19206ce24a7b32e",
        "Accept": "text/event-stream",
        "Content-Type": "application/json",
    }

    session_id = f"{episode_id}-1"
    task_id = generate_uuid()

    payload = {
        "sessionId": session_id,
        "projectId": project_id,
        "episodeId": episode_id,
        "workspaceId": workspace_id,
        "param": {
            "text": text,
            "character": [],
            "scene": [],
            "ratio": "9:16",
            "mode": "one-click",
            "file": [],
            "parsedImageContents": [],
            "parsedPdfContents": [],
            "taskId": task_id,
            "role": "user",
            "type": "ai_story",
            "status": "success",
            "sessionId": session_id,
            "uuid": "",
            "workspaceId": workspace_id,
        },
    }

    data = json.dumps(payload).encode("utf-8")
    req = urllib.request.Request(url=url, data=data, headers=headers, method="POST")

    with urllib.request.urlopen(req) as resp:
        for raw_line in resp:
            line = raw_line.decode("utf-8").strip()
            if "disconnect" not in line:
                continue
            print(line, file=sys.stderr)


def init_tracks(token: str, workspace_id: str) -> None:
    url = f"https://bole.bonanai.com/api/bkk/tracks/init?workspaceId={workspace_id}"

    headers = {
        "Authorization": f"Bearer {token}",
        "ClientID": "e5cd7e4891bf95d1d19206ce24a7b32e",
        "Accept": "application/json, text/plain, */*",
    }

    req = urllib.request.Request(url=url, headers=headers, method="GET")

    with urllib.request.urlopen(req) as resp:
        resp_body = resp.read().decode("utf-8")

    resp_json = json.loads(resp_body)
    print(f"init tracks res: {resp_json}", file=sys.stderr)


def init_videos(token: str, workspace_id: str) -> None:
    url = f"https://bole.bonanai.com/api/bkk/tracks/generateVideo?workspaceId={workspace_id}"

    headers = {
        "Authorization": f"Bearer {token}",
        "ClientID": "e5cd7e4891bf95d1d19206ce24a7b32e",
        "Accept": "application/json, text/plain, */*",
    }

    req = urllib.request.Request(url=url, headers=headers, method="GET")

    with urllib.request.urlopen(req) as resp:
        resp_body = resp.read().decode("utf-8")

    resp_json = json.loads(resp_body)
    print(f"init videos res: {resp_json}", file=sys.stderr)


def final_edit(token: str, workspace_id: str) -> None:
    url = f"https://bole.bonanai.com/api/bkk/tracks/resetFinalVideoStatus?workspaceId={workspace_id}"

    headers = {
        "Authorization": f"Bearer {token}",
        "ClientID": "e5cd7e4891bf95d1d19206ce24a7b32e",
        "Accept": "application/json, text/plain, */*",
    }

    req = urllib.request.Request(url=url, headers=headers, method="GET")

    with urllib.request.urlopen(req) as resp:
        resp_body = resp.read().decode("utf-8")

    resp_json = json.loads(resp_body)
    print(f"final edit res: {resp_json}", file=sys.stderr)


def get_tracks(token: str, workspace_id: str) -> bool:
    url = f"https://bole.bonanai.com/api/bkk/tracks/getTracks?workspaceId={workspace_id}"

    headers = {
        "Authorization": f"Bearer {token}",
        "ClientID": "e5cd7e4891bf95d1d19206ce24a7b32e",
        "Accept": "application/json, text/plain, */*",
    }

    req = urllib.request.Request(url=url, headers=headers, method="GET")

    with urllib.request.urlopen(req) as resp:
        resp_body = resp.read().decode("utf-8")

    resp_json = json.loads(resp_body)
    tracks = resp_json.get("data", [])
    # 判断每个track的resource字段是否有值，都有值则返回true
    all_tracks_ready = bool(tracks) and all(track.get("resource") for track in tracks)
    print(f"tracks ready: {all_tracks_ready}", file=sys.stderr)
    return all_tracks_ready


def check_final_video_status(token: str, workspace_id: str) -> bool:
    url = f"https://bole.bonanai.com/api/bkk/tracks/startFinalVideo?workspaceId={workspace_id}"

    headers = {
        "Authorization": f"Bearer {token}",
        "ClientID": "e5cd7e4891bf95d1d19206ce24a7b32e",
        "Accept": "application/json, text/plain, */*",
    }

    req = urllib.request.Request(url=url, headers=headers, method="GET")

    with urllib.request.urlopen(req) as resp:
        resp_body = resp.read().decode("utf-8")

    resp_json = json.loads(resp_body)
    data = resp_json.get("data", {})
    # 判断data.status是否为9
    status = data.get("status", -1)
    print(f"final video status: {status}", file=sys.stderr)
    return status == 9


def get_final_video(token: str, workspace_id: str) -> str:
    url = f"https://bole.bonanai.com/api/bkk/project/getWorkspaceById?workspaceId={workspace_id}"

    headers = {
        "Authorization": f"Bearer {token}",
        "ClientID": "e5cd7e4891bf95d1d19206ce24a7b32e",
        "Accept": "application/json, text/plain, */*",
    }

    req = urllib.request.Request(url=url, headers=headers, method="GET")

    with urllib.request.urlopen(req) as resp:
        resp_body = resp.read().decode("utf-8")

    resp_json = json.loads(resp_body)
    data = resp_json.get("data", {})
    finalVideo = data.get("finalVideo", {})
    finalVideoList = finalVideo.get("finalVideoList", [])
    url = finalVideoList[0].get("url", "") if finalVideoList else ""
    print(f"final video url: {url}", file=sys.stderr)
    return url


def main(inputs):
    text = inputs.get("text")
    if not text:
        return {"error": "text is required"}
    
    try:
        token = create_access_token()
        project_id = "2033716579396616193"
        print(f"projectId: {project_id}", file=sys.stderr)
        episode_id = create_episode(token, project_id)
        workspace_id = create_workspace(token, project_id, episode_id)
        time.sleep(10)

        create_storyboard(token, project_id, episode_id, workspace_id, text)

        init_tracks(token, workspace_id)
        while not get_tracks(token, workspace_id):
            time.sleep(10)
        
        init_videos(token, workspace_id)
        while not get_tracks(token, workspace_id):
            time.sleep(10)
        
        final_edit(token, workspace_id)
        while not check_final_video_status(token, workspace_id):
            time.sleep(10)
        
        final_video_url = get_final_video(token, workspace_id)

        result = f"故事创作完成！projectId={project_id}, episodeId={episode_id}, workspaceId={workspace_id}。控制台链接：https://bole.bonanai.com/story/{project_id}?episodeId={episode_id} 。视频链接：{final_video_url}"
        return {"result": result}
    except Exception as e:
        return {"error": str(e)}


if __name__ == "__main__":
    import sys
    if len(sys.argv) > 1:
        try:
            inputs = json.loads(sys.argv[1])
            result = main(inputs)
            print(json.dumps(result))
        except json.JSONDecodeError:
            print(json.dumps({"error": "Invalid JSON input"}))
        except Exception as e:
            print(json.dumps({"error": str(e)}))
    else:
        print(json.dumps({"error": "No input provided"}))