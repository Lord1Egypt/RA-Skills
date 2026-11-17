"""Interactive demo: control Music.app from your terminal."""

import json
import subprocess
import time


def music(cmd: str) -> str:
    result = subprocess.run(
        ["app-agent-music"] + cmd.split(),
        capture_output=True, text=True, timeout=15,
    )
    return result.stdout.strip()


def search_and_play(keyword: str) -> str:
    """Search library for a song and play the first match."""
    script = f'''
tell application "Music"
    set results to every track of library playlist 1 whose name contains "{keyword}"
    if results is not {{}} then
        play item 1 of results
        set t to item 1 of results
        return (name of t) & " - " & (artist of t)
    else
        return "未找到"
    end if
end tell
'''
    result = subprocess.run(
        ["osascript", "-e", script],
        capture_output=True, text=True, timeout=15,
    )
    return result.stdout.strip() or result.stderr.strip()


def main():
    print("\n🎵 Music.app 远程控制 Demo\n")

    # 1. 打开 Music 并放到前台
    print("▸ 打开 Music.app 并置于前台")
    music("set-frontmost true")
    time.sleep(1)
    print(f"  应用: {music('get-name')} v{music('get-version')}")
    print(f"  状态: {music('get-player-state')}")
    print(f"  音量: {music('get-sound-volume')}")

    # 2.
    time.sleep(2)

    # 3. 调节音量
    print("\n▸ 调节音量 → 50")
    music("set-sound-volume 50")
    print(f"  音量: {music('get-sound-volume')}")

    # 4. 搜索「大城小爱」并播放
    print("\n▸ 搜索「大城小爱」并播放")
    match = search_and_play("大城小爱")
    print(f"  匹配: {match}")
    time.sleep(1)
    print(f"  状态: {music('get-player-state')}")
    print("  ♪ 播放中 ...")
    time.sleep(8)

    # 5. 下一首
    print("\n▸ 下一首")
    music("next-track")
    time.sleep(2)
    print(f"  切换到: {music('get-current-track-name')} - {music('get-current-track-artist')}")
    print("  ♪ 播放中 ...")
    time.sleep(8)

    # 6. 获取当前曲目信息（复合 JSON 命令）
    print("\n▸ 当前曲目详情")
    raw = music("--json get-current-track")
    try:
        for k, v in json.loads(raw).items():
            print(f"  {k}: {v}")
    except Exception:
        print(f"  {raw}")

    # 7.
    time.sleep(2)

    # 8. 停止播放，恢复音量
    print("\n▸ 停止播放，恢复音量")
    music("stop")
    music("set-sound-volume 73")
    print(f"  状态: {music('get-player-state')}")
    print(f"  音量: {music('get-sound-volume')}")

    print("\n✅ Demo 结束\n")


if __name__ == "__main__":
    main()
