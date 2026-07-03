#!/usr/bin/env python3
"""
bili-harvest.py — bilibili 收割编排

工作流:
  hot  <keyword>            搜主题 → 按指定 order 拿候选 → 逐条 video → 落盘 + REPORT
  user <mid>                UP 主主页 → 拿 N 条视频 → 逐条 video → 落盘 + REPORT
  ids  <bvid> [<bvid> ...]  已知 BV 号批量抓 → 落盘 + REPORT

数据落盘:
  $SKILL/data/harvests/<topic>-<时间戳>/
  ├── REPORT.md             人类可读报告 (含热门评论样本)
  ├── search.json           搜索结果 / UP 主候选
  ├── user.json             (仅 user 模式) UP 主元数据
  └── videos/
      ├── v01-<bvid前6>.json
      └── ...

设计:
  - 内调 bili-fetch.py 子命令,自己只做编排
  - 限速: 视频之间 sleep 1s (B 站抓取温和,比 xhs 宽松)
  - 失败: 单条失败不中断,记到 errors
  - REPORT.md 包含: 元信息 + 视频表 + 每条 top 3 评论
"""

import argparse
import json
import re
import subprocess
import sys
import time
from datetime import datetime
from pathlib import Path

from paths import HARVESTS_DIR


# 优先用同目录的 venv 里的 python (bilibili-api 库仅装在 venv)
_VENV_PY = Path(__file__).parent / '.venv' / 'bin' / 'python'
_PY = str(_VENV_PY) if _VENV_PY.exists() else sys.executable


# ============== 工具 ==============

def err(msg):
    print(f"❌ {msg}", file=sys.stderr)


def ok(msg):
    print(f"✅ {msg}")


def info(msg):
    print(f"  {msg}")


def now_ts():
    return datetime.now().strftime("%Y%m%d-%H%M%S")


def parse_date_arg(s):
    """解析 --since / --before 用的日期字符串 → Unix ts (00:00:00 UTC)

    接受的格式:
      YYYY-MM-DD        → 当天 00:00:00 UTC
      YYYY-MM-DDTHH:MM  → 带小时 (本地时区)
      YYYY-MM-DD HH:MM  → 同上 (无 T)

    返回 int(unix ts) 或 None(空或解析失败)
    """
    s = (s or '').strip()
    if not s:
        return None
    s = s.replace('T', ' ')
    from datetime import datetime
    for fmt in ('%Y-%m-%d %H:%M', '%Y-%m-%d'):
        try:
            dt = datetime.strptime(s, fmt)
            return int(dt.timestamp())
        except ValueError:
            continue
    err(f"无法解析日期 {s!r}, 期望 YYYY-MM-DD")
    return None


def fetch_one(bvid, comments=10, danmaku=False, danmaku_dir=None):
    """调 bili-fetch.py video 拿一条视频 + 评论 (+ 可选弹幕) (走 --out 临时文件, JSON 干净)

    danmaku_dir: 如果提供, 把弹幕落盘到 <danmaku_dir>/<bvid>.json
    """
    import tempfile
    tmp = tempfile.NamedTemporaryFile('w', suffix='.json', delete=False)
    tmp.close()
    cmd = [
        _PY, str(Path(__file__).parent / 'bili-fetch.py'),
        'video', bvid, '--comments', str(comments),
    ]
    if danmaku and danmaku_dir is not None:
        dmpath = Path(danmaku_dir) / f"{bvid}.json"
        dmpath.parent.mkdir(parents=True, exist_ok=True)
        cmd += ['--danmaku-out', str(dmpath)]
    cmd += ['--out', tmp.name]
    r = subprocess.run(
        cmd,
        capture_output=True, text=True, timeout=180,
    )
    data = None
    if r.returncode == 0:
        try:
            data = json.loads(Path(tmp.name).read_text())
        except (json.JSONDecodeError, FileNotFoundError):
            pass
    Path(tmp.name).unlink(missing_ok=True)
    return r.returncode, data, r.stderr


# ============== harvest 子命令 ==============

def cmd_hot(args):
    """主题热门收割"""
    keyword = args.keyword
    info(f"收割主题: {keyword!r}  order={args.order}  limit={args.limit}  comments={args.comments}  danmaku={args.danmaku}")

    # Step 1: 搜索拿候选 (走 --out 临时文件)
    import tempfile
    tmp = tempfile.NamedTemporaryFile('w', suffix='.json', delete=False)
    tmp.close()
    r = subprocess.run(
        [_PY, str(Path(__file__).parent / 'bili-fetch.py'),
         'search', keyword, '--order', args.order,
         '--ps', str(args.ps), '--pages', str(args.pages),
         '--out', tmp.name],
        capture_output=True, text=True, timeout=60,
    )
    if r.returncode != 0:
        err(f"搜索失败: {r.stderr}")
        Path(tmp.name).unlink(missing_ok=True)
        return 1
    try:
        search_data = json.loads(Path(tmp.name).read_text())
    except (json.JSONDecodeError, FileNotFoundError) as e:
        err(f"搜索 JSON 解析失败: {e}")
        Path(tmp.name).unlink(missing_ok=True)
        return 1
    Path(tmp.name).unlink(missing_ok=True)
    candidates = search_data.get('items', [])[:args.limit]
    if not candidates:
        err("搜索没结果")
        return 1
    info(f"候选 {len(candidates)} 条")

    # Step 2: 落盘目录
    safe_kw = re.sub(r'[^\w\-]', '_', keyword)[:30]
    out_dir = HARVESTS_DIR / f"hot-{safe_kw}-{args.order}-{now_ts()}"
    (out_dir / 'videos').mkdir(parents=True, exist_ok=True)
    danmaku_dir = out_dir / 'danmaku'
    with open(out_dir / 'search.json', 'w', encoding='utf-8') as f:
        json.dump(search_data, f, ensure_ascii=False, indent=2)

    # Step 3: 逐条抓详情
    videos = []
    errors = []
    for i, c in enumerate(candidates, 1):
        bvid = c['bvid']
        info(f"[{i}/{len(candidates)}] {bvid}  {c['title'][:30]}")
        rc, data, err_out = fetch_one(bvid, args.comments, danmaku=args.danmaku, danmaku_dir=danmaku_dir)
        if rc != 0 or data is None:
            err(f"  失败: {(err_out or '')[:200]}")
            errors.append({'bvid': bvid, 'error': (err_out or '')[:200]})
            continue
        videos.append(data)
        # 落盘单条
        with open(out_dir / 'videos' / f"v{i:02d}-{bvid[:8]}.json", 'w', encoding='utf-8') as f:
            json.dump(data, f, ensure_ascii=False, indent=2)
        time.sleep(args.sleep)

    # Step 4: 写 REPORT.md
    write_report_hot(out_dir, keyword, args, candidates, videos, errors)
    ok(f"完成 → {out_dir}")
    return 0


def write_report_hot(out_dir, keyword, args, candidates, videos, errors):
    path = out_dir / 'REPORT.md'
    with open(path, 'w', encoding='utf-8') as f:
        f.write(f"# B 站收割报告: 「{keyword}」\n\n")
        f.write(f"- 关键词: `{keyword}`\n")
        f.write(f"- 排序: `{args.order}`\n")
        f.write(f"- 抓取时间: {datetime.now().isoformat(timespec='seconds')}\n")
        f.write(f"- 候选 {len(candidates)} 条, 成功 {len(videos)} 条, 失败 {len(errors)} 条\n")
        f.write(f"- 抓取参数: limit={args.limit}, comments={args.comments}, sleep={args.sleep}s\n\n")

        f.write("## 视频列表\n\n")
        f.write("| # | 标题 | UP 主 | 时长 | 播放 | 弹幕 | 评论 | BV |\n")
        f.write("|---|---|---|---|---|---|---|---|\n")
        for i, v in enumerate(videos, 1):
            st = v.get('stat', {})
            f.write(f"| {i} | {v.get('title', '')[:40]} | {v.get('owner', {}).get('name', '')} "
                    f"| {v.get('duration_text', '')} | {st.get('view', '')} "
                    f"| {st.get('danmaku', '')} | {st.get('reply', '')} | `{v.get('bvid', '')}` |\n")
        if errors:
            f.write("\n## 失败列表\n\n")
            for e in errors:
                f.write(f"- `{e['bvid']}`: {e['error']}\n")

        # 热门评论样本 (每条前 3)
        f.write("\n## 热门评论样本 (每条 top 3)\n\n")
        for i, v in enumerate(videos, 1):
            f.write(f"### {i}. {v.get('title', '')}\n\n")
            samples = v.get('comments_sample', [])
            if not samples:
                f.write("_无评论样本_\n\n")
                continue
            for c in samples:
                loc = f" [{c.get('location')}]" if c.get('location') else ''
                f.write(f"- **{c['uname']}**{loc} (👍{c['like']}): {c['content']}\n")
            f.write("\n")

        # 弹幕统计
        if args.danmaku:
            dm_count = 0
            dm_files = 0
            danmaku_dir = out_dir / 'danmaku'
            if danmaku_dir.exists():
                dm_files = len(list(danmaku_dir.glob('*.json')))
                for fp in danmaku_dir.glob('*.json'):
                    try:
                        dm_count += len(json.loads(fp.read_text()))
                    except Exception:
                        pass
            f.write("\n## 弹幕统计\n\n")
            f.write(f"- 文件: `data/harvests/{out_dir.name}/danmaku/`, 共 **{dm_files}** 个 BV\n")
            f.write(f"- 总弹幕数: **{dm_count}** 条\n")
            if dm_files and videos:
                f.write(f"- 平均: {dm_count // max(dm_files,1)} 条/视频\n\n")


def cmd_user(args):
    """UP 主视频收割"""
    mid = str(args.mid)
    m = re.search(r'space\.bilibili\.com/(\d+)', mid)
    if m:
        mid = m.group(1)
    info(f"收割 UP 主: mid={mid}  videos={args.videos}  comments={args.comments}  danmaku={args.danmaku}")

    # 时间过滤参数 (--since / --before) 在这里解析, 后面早终止用
    since_ts = parse_date_arg(args.since)
    before_ts = parse_date_arg(args.before)
    if args.since or args.before:
        info(f"时间过滤: {args.since or '(无下限)'} → {args.before or '(无上限)'}")

    # Step 1: 拿 UP 主主页 (走 --out 临时文件, harvest 只取 JSON)
    import tempfile
    tmp_user = tempfile.NamedTemporaryFile('w', suffix='.json', delete=False)
    tmp_user.close()
    user_cmd = [_PY, str(Path(__file__).parent / 'bili-fetch.py'),
         'user', mid, '--videos', str(args.videos)]
    if args.auto_pages:
        user_cmd.append('--scroll')
    user_cmd += ['--out', tmp_user.name]
    r = subprocess.run(
        user_cmd,
        capture_output=True, text=True, timeout=180,
    )
    if r.returncode != 0:
        err(f"UP 主主页失败: {r.stderr}")
        Path(tmp_user.name).unlink(missing_ok=True)
        return 1
    try:
        user_data = json.loads(Path(tmp_user.name).read_text())
    except (json.JSONDecodeError, FileNotFoundError) as e:
        err(f"用户 JSON 解析失败: {e}")
        Path(tmp_user.name).unlink(missing_ok=True)
        return 1
    Path(tmp_user.name).unlink(missing_ok=True)
    candidates = user_data.get('videos', [])
    if not candidates:
        err("UP 主没拿到视频列表")
        return 1
    info(f"UP 主 {user_data.get('name', mid)}  候选 {len(candidates)} 条")

    # Step 2: 落盘
    out_dir = HARVESTS_DIR / f"user-{mid[:12]}-{now_ts()}"
    (out_dir / 'videos').mkdir(parents=True, exist_ok=True)
    danmaku_dir = out_dir / 'danmaku'
    with open(out_dir / 'user.json', 'w', encoding='utf-8') as f:
        json.dump(user_data, f, ensure_ascii=False, indent=2)

    # Step 3: 逐条抓 (时间过滤 + 早终止)
    # 策略: B 站 UP 主空间默认按时间倒序, 进入 since 前的第一条之后都跳过 (节省调用)
    videos = []
    errors = []
    skipped_after = 0  # 早于 since 被跳过的数量 (供 REPORT 显示)
    time_filter_active = since_ts is not None or before_ts is not None
    for i, c in enumerate(candidates, 1):
        bvid = c['bvid']
        info(f"[{i}/{len(candidates)}] {bvid}  {c['title'][:30]}")
        rc, data, err_out = fetch_one(bvid, args.comments, danmaku=args.danmaku, danmaku_dir=danmaku_dir)
        if rc != 0 or data is None:
            errors.append({'bvid': bvid, 'error': (err_out or '')[:200]})
            continue

        # 时间过滤 (使用 video 接口返回的精确 pubdate)
        if time_filter_active:
            pub_ts = data.get('pubdate')
            pub_text = data.get('pubdate_text', '?')
            if pub_ts is not None:
                if since_ts is not None and pub_ts < since_ts:
                    info(f"  ⏹ {pub_text} 早于 {args.since}, 本 bvid 及之后停止 (倒序假设)")
                    skipped_after = len(candidates) - i + 1
                    break
                if before_ts is not None and pub_ts > before_ts:
                    info(f"  ⏭ {pub_text} 晚于 {args.before}, 跳过")
                    continue

        videos.append(data)
        with open(out_dir / 'videos' / f"v{i:02d}-{bvid[:8]}.json", 'w', encoding='utf-8') as f:
            json.dump(data, f, ensure_ascii=False, indent=2)
        time.sleep(args.sleep)

    # Step 4: REPORT
    write_report_user(out_dir, user_data, videos, errors, args, skipped_after=skipped_after)
    ok(f"完成 → {out_dir}")
    return 0


def write_report_user(out_dir, user_data, videos, errors, args, skipped_after=0):
    path = out_dir / 'REPORT.md'
    with open(path, 'w', encoding='utf-8') as f:
        f.write(f"# B 站收割报告: UP 主「{user_data.get('name', args.mid)}」\n\n")
        f.write(f"- UP 主: {user_data.get('name', '')} (mid={user_data.get('mid', args.mid)})\n")
        f.write(f"- 签名: {user_data.get('sign', '')}\n")
        f.write(f"- 粉丝: {user_data.get('fans', '?')}  关注: {user_data.get('follow', '?')}\n")
        f.write(f"- 主页: {user_data.get('space_url', '')}\n")
        f.write(f"- 抓取时间: {datetime.now().isoformat(timespec='seconds')}\n")
        if args.since or args.before:
            f.write(f"- 时间过滤: **{args.since or '最早'} → {args.before or '最晚'}**\n")
            f.write(f"- (因早终止跳过 {skipped_after} 条 earliest-than-since 的 bvid)\n" if skipped_after else f"- 时间过滤生效, 共跳过 {skipped_after} 条\n")
        f.write(f"- 候选 {len(user_data.get('videos', []))} 条, 成功 {len(videos)} 条, 失败 {len(errors)} 条\n\n")

        f.write("## 视频列表\n\n")
        f.write("| # | 日期 | 标题 | 时长 | 播放 | 弹幕 | 评论 | BV |\n")
        f.write("|---|---|---|---|---|---|---|---|\n")
        for i, v in enumerate(videos, 1):
            st = v.get('stat', {})
            date = v.get('pubdate_text') or '?'
            f.write(f"| {i} | {date} | {v.get('title', '')[:40]} | {v.get('duration_text', '')} "
                    f"| {st.get('view', '')} | {st.get('danmaku', '')} | {st.get('reply', '')} | `{v.get('bvid', '')}` |\n")
        if errors:
            f.write("\n## 失败列表\n\n")
            for e in errors:
                f.write(f"- `{e['bvid']}`: {e['error']}\n")

        f.write("\n## 热门评论样本 (每条 top 3)\n\n")
        for i, v in enumerate(videos, 1):
            f.write(f"### {i}. {v.get('title', '')}\n\n")
            samples = v.get('comments_sample', [])
            if not samples:
                f.write("_无评论样本_\n\n")
                continue
            for c in samples:
                loc = f" [{c.get('location')}]" if c.get('location') else ''
                f.write(f"- **{c['uname']}**{loc} (👍{c['like']}): {c['content']}\n")
            f.write("\n")

        # 弹幕统计
        if args.danmaku:
            dm_count = 0
            dm_files = 0
            danmaku_dir = out_dir / 'danmaku'
            if danmaku_dir.exists():
                dm_files = len(list(danmaku_dir.glob('*.json')))
                for fp in danmaku_dir.glob('*.json'):
                    try:
                        dm_count += len(json.loads(fp.read_text()))
                    except Exception:
                        pass
            f.write("\n## 弹幕统计\n\n")
            f.write(f"- 文件: `data/harvests/{out_dir.name}/danmaku/`, 共 **{dm_files}** 个 BV\n")
            f.write(f"- 总弹幕数: **{dm_count}** 条\n")
            if dm_files and videos:
                f.write(f"- 平均: {dm_count // max(dm_files,1)} 条/视频\n\n")


def cmd_ids(args):
    """已知 BV 号批量抓"""
    bvids = list(args.bvids)
    info(f"批量抓 {len(bvids)} 条  comments={args.comments}  danmaku={args.danmaku}")

    out_dir = HARVESTS_DIR / f"ids-{now_ts()}"
    (out_dir / 'videos').mkdir(parents=True, exist_ok=True)
    danmaku_dir = out_dir / 'danmaku'

    videos = []
    errors = []
    for i, bvid in enumerate(bvids, 1):
        info(f"[{i}/{len(bvids)}] {bvid}")
        rc, data, err_out = fetch_one(bvid, args.comments, danmaku=args.danmaku, danmaku_dir=danmaku_dir)
        if rc != 0 or data is None:
            errors.append({'bvid': bvid, 'error': (err_out or '')[:200]})
            continue
        videos.append(data)
        with open(out_dir / 'videos' / f"v{i:02d}-{bvid[:8]}.json", 'w', encoding='utf-8') as f:
            json.dump(data, f, ensure_ascii=False, indent=2)
        time.sleep(args.sleep)

    # 简单 REPORT
    path = out_dir / 'REPORT.md'
    with open(path, 'w', encoding='utf-8') as f:
        f.write("# B 站批量收割报告\n\n")
        f.write(f"- 抓取时间: {datetime.now().isoformat(timespec='seconds')}\n")
        f.write(f"- 输入 {len(bvids)} 条, 成功 {len(videos)} 条, 失败 {len(errors)} 条\n\n")
        f.write("## 视频列表\n\n")
        f.write("| # | 标题 | UP 主 | 播放 | 评论 | BV |\n|---|---|---|---|---|---|\n")
        for i, v in enumerate(videos, 1):
            st = v.get('stat', {})
            f.write(f"| {i} | {v.get('title', '')[:40]} | {v.get('owner', {}).get('name', '')} "
                    f"| {st.get('view', '')} | {st.get('reply', '')} | `{v.get('bvid', '')}` |\n")
        if errors:
            f.write("\n## 失败列表\n\n")
            for e in errors:
                f.write(f"- `{e['bvid']}`: {e['error']}\n")
        f.write("\n## 热门评论样本\n\n")
        for i, v in enumerate(videos, 1):
            f.write(f"### {i}. {v.get('title', '')}\n\n")
            for c in v.get('comments_sample', []):
                f.write(f"- **{c['uname']}** (👍{c['like']}): {c['content']}\n")
            f.write("\n")

        # 弹幕统计
        if args.danmaku:
            dm_count = 0
            dm_files = 0
            if danmaku_dir.exists():
                dm_files = len(list(danmaku_dir.glob('*.json')))
                for fp in danmaku_dir.glob('*.json'):
                    try:
                        dm_count += len(json.loads(fp.read_text()))
                    except Exception:
                        pass
            f.write("\n## 弹幕统计\n\n")
            f.write(f"- 文件: `data/harvests/{out_dir.name}/danmaku/`, 共 **{dm_files}** 个 BV\n")
            f.write(f"- 总弹幕数: **{dm_count}** 条\n\n")

    ok(f"完成 → {out_dir}")
    return 0


# ============== 主入口 ==============

def main():
    p = argparse.ArgumentParser(
        description='bilibili 收割编排 (搜主题 / UP 主 / 已知BV号 → 逐条 video → 落盘 + REPORT)',
        formatter_class=argparse.RawDescriptionHelpFormatter,
        epilog="""子命令:
  hot  <keyword>             搜主题 → 候选 → 逐条抓
  user <mid>                 UP 主主页 → 候选 → 逐条抓
  ids  <bvid> [<bvid> ...]   已知 BV 号批量抓

示例:
  bili-harvest.py hot "逗比的雀巢" --order pubdate --limit 10 --comments 15
  bili-harvest.py user 5294454 --videos 40 --comments 20
  bili-harvest.py ids BV1K3Gz6pEoo BV16ooQBsERA
"""
    )
    sub = p.add_subparsers(dest='cmd', required=True)

    # hot
    p1 = sub.add_parser('hot', help='搜主题热门收割')
    p1.add_argument('keyword', help='关键词')
    p1.add_argument('--order', default='totalrank',
                    choices=['totalrank', 'click', 'pubdate', 'dm', 'stow', 'vv',
                             'favorite', 'hot'],
                    help='排序 (默认 totalrank)')
    p1.add_argument('--limit', type=int, default=10, help='最多抓多少条 (默认 10)')
    p1.add_argument('--ps', type=int, default=20, help='搜索每页条数 (默认 20)')
    p1.add_argument('--pages', type=int, default=1, help='搜索翻几页 (默认 1)')
    p1.add_argument('--comments', type=int, default=10, help='每条抓几个评论 (默认 10)')
    p1.add_argument('--danmaku', action='store_true', help='额外抓弹幕 (需 bilibili-api 库)')
    p1.add_argument('--sleep', type=float, default=1.0, help='视频之间间隔秒 (默认 1.0)')

    # user
    p2 = sub.add_parser('user', help='UP 主视频收割')
    p2.add_argument('mid', help='UP 主 mid 或 space URL')
    p2.add_argument('--videos', type=int, default=20, help='最多抓多少条 (默认 20)')
    p2.add_argument('--comments', type=int, default=10, help='每条抓几个评论 (默认 10)')
    p2.add_argument('--danmaku', action='store_true', help='额外抓弹幕 (需 bilibili-api 库)')
    p2.add_argument('--sleep', type=float, default=1.0, help='视频之间间隔秒 (默认 1.0)')
    p2.add_argument('--since', metavar='YYYY-MM-DD', default=None,
                    help='只看该日期之后的视频 (含)。传了之后会 早终止 提前出结果。')
    p2.add_argument('--before', metavar='YYYY-MM-DD', default=None,
                    help='只看该日期之前的视频 (含)')
    p2.add_argument('--auto-pages', '--scroll', dest='auto_pages', action='store_true',
                    help='启用后, 会传递 --scroll 给 fetch.py user, 让它自动滚到底拿全量 (推荐配合 --since 使用)')

    # ids
    p3 = sub.add_parser('ids', help='已知 BV 号批量抓')
    p3.add_argument('bvids', nargs='+', help='BV 号列表 (空格分隔)')
    p3.add_argument('--comments', type=int, default=10, help='每条抓几个评论 (默认 10)')
    p3.add_argument('--danmaku', action='store_true', help='额外抓弹幕 (需 bilibili-api 库)')
    p3.add_argument('--sleep', type=float, default=1.0, help='视频之间间隔秒 (默认 1.0)')

    args = p.parse_args()
    fn = globals().get(f"cmd_{args.cmd}")
    if not fn:
        err(f"未知子命令: {args.cmd}")
        return 1
    return fn(args) or 0


if __name__ == '__main__':
    sys.exit(main())