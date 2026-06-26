#!/usr/bin/env python3
"""
Douyin Reverse Engineer - 从视频反推AI绘画提示词和分镜脚本

用法：
  # 完整流程（下载 + 分析）
  python reverse_video.py "https://www.douyin.com/video/xxx"

  # 分析本地视频（跳过下载）
  python reverse_video.py --local ./video.mp4

  # 仅下载（不分析）
  python reverse_video.py "https://www.douyin.com/video/xxx" --download-only

  # 自定义输出目录
  python reverse_video.py "URL" --output ./out

  # 跳过游戏向改写
  python reverse_video.py "URL" --no-rewrite

  # 启用锈湖风格大模型改写
  python reverse_video.py "URL" --rusty-lake
"""

import os
import sys
import re
import csv
import json
import argparse
import subprocess

# Windows 控制台编码修复
if sys.platform == 'win32':
    sys.stdout.reconfigure(encoding='utf-8', errors='replace')
    sys.stderr.reconfigure(encoding='utf-8', errors='replace')


# ---------------------------------------------------------------------------
# 路径工具
# ---------------------------------------------------------------------------

def _project_root():
    """返回项目根目录（即 skills/ 的父目录）"""
    return os.path.abspath(os.path.join(os.path.dirname(__file__), '..', '..'))


def _douyin_downloader_script():
    return os.path.join(_project_root(), 'skills', 'douyin-downloader', 'scripts', 'douyin_download.py')


def _video_downloader_script():
    return os.path.join(_project_root(), 'skills', 'video-downloader', 'scripts', 'video_downloader.py')


def _video_analyzer_script():
    return os.path.join(_project_root(), 'skills', 'doubao-video-analyzer', 'script', 'parse_video.py')


# ---------------------------------------------------------------------------
# 模块1 - 视频下载
# ---------------------------------------------------------------------------

def _is_douyin_url(url):
    """判断是否为抖音链接"""
    return bool(re.search(r'douyin\.com|v\.douyin\.com', url))


def _extract_video_id(url):
    """从抖音 URL 中提取视频 ID（aweme_id / modal_id）"""
    # https://www.douyin.com/video/7619689757290843419
    m = re.search(r'/video/(\d+)', url)
    if m:
        return m.group(1)
    # https://www.douyin.com/jingxuan?modal_id=7597329042169220398
    m = re.search(r'modal_id[=:](\d+)', url)
    if m:
        return m.group(1)
    # 纯数字
    m = re.match(r'^(\d{16,})$', url.strip())
    if m:
        return m.group(1)
    return None


def download_douyin(url, output_dir):
    """
    通过 douyin-downloader skill（TikHub API）下载抖音视频。

    参数：
        url:        抖音视频链接或 modal_id
        output_dir: 下载文件保存目录

    返回：
        本地视频文件路径（str）
    """
    # 将 douyin-downloader 脚本所在目录加入 sys.path 以便 import
    script_dir = os.path.dirname(_douyin_downloader_script())
    if script_dir not in sys.path:
        sys.path.insert(0, script_dir)

    from douyin_download import get_video_info, download_video as _dl_video

    video_id = _extract_video_id(url) or url
    print(f'[下载] 抖音视频 ID: {video_id}')
    print(f'[下载] 调用 TikHub API 获取视频直链 ...')

    info = get_video_info(video_id)
    video_url = info['video_url']
    print(f'[下载] 获取到视频直链: {video_url[:80]}...')

    os.makedirs(output_dir, exist_ok=True)
    output_path = os.path.join(output_dir, f'douyin_{info["modal_id"]}.mp4')

    print(f'[下载] 正在下载视频 ...')
    _dl_video(video_url, output_path)

    size_mb = os.path.getsize(output_path) / (1024 * 1024)
    print(f'[下载] 完成: {output_path} ({size_mb:.1f} MB)')
    return output_path


def download_general(url, output_dir, resolution='1080p'):
    """
    通过 video-downloader skill（yt-dlp）下载非抖音平台视频。

    参数：
        url:        视频页面链接（YouTube / B站 等）
        output_dir: 下载文件保存目录
        resolution: 目标分辨率，默认 1080p

    返回：
        本地视频文件路径（str）
    """
    script_path = _video_downloader_script()
    if not os.path.isfile(script_path):
        raise FileNotFoundError(
            f'找不到 video-downloader skill，请先安装: npx clawhub install video-downloader'
        )

    os.makedirs(output_dir, exist_ok=True)

    cmd = [sys.executable, script_path, url, resolution, output_dir]
    print(f'[下载] 调用 video-downloader (yt-dlp) ...')

    result = subprocess.run(
        cmd,
        capture_output=True,
        timeout=600,
    )

    stdout_text = result.stdout.decode('utf-8', errors='replace')
    stderr_text = result.stderr.decode('utf-8', errors='replace')

    if stdout_text.strip():
        for line in stdout_text.strip().splitlines():
            print(f'  [video-downloader] {line}')
    if stderr_text.strip():
        for line in stderr_text.strip().splitlines():
            print(f'  [video-downloader:err] {line}')

    if result.returncode != 0:
        raise RuntimeError(f'video-downloader 退出码 {result.returncode}')

    # 从输出中解析 "最终文件: xxx"
    video_path = _parse_final_path(stdout_text)
    if video_path and os.path.isfile(video_path):
        print(f'[下载] 完成: {video_path}')
        return video_path

    # 备选：扫描目录
    video_path = _find_video_in_dir(output_dir)
    if video_path:
        print(f'[下载] 完成（目录扫描）: {video_path}')
        return video_path

    raise RuntimeError(f'下载完成但未找到视频文件，请检查: {output_dir}')


def download_video(url, output_dir, resolution='1080p'):
    """
    统一下载入口：抖音链接走 TikHub API，其他平台走 yt-dlp。
    """
    if _is_douyin_url(url) or re.match(r'^\d{16,}$', url.strip()):
        return download_douyin(url, output_dir)
    else:
        return download_general(url, output_dir, resolution)


def _parse_final_path(stdout_text):
    """从 video_downloader.py 的标准输出中解析 '最终文件: xxx' 行"""
    for line in stdout_text.splitlines():
        m = re.search(r'最终文件:\s*(.+)', line)
        if m:
            return m.group(1).strip()
    return None


def _find_video_in_dir(directory):
    """在目录中查找最新的视频文件"""
    video_exts = ('.mp4', '.mkv', '.webm', '.mov', '.avi')
    candidates = []
    for f in os.listdir(directory):
        if any(f.lower().endswith(ext) for ext in video_exts):
            full = os.path.join(directory, f)
            candidates.append((os.path.getmtime(full), full))
    if candidates:
        candidates.sort(reverse=True)
        return candidates[0][1]
    return None


# ---------------------------------------------------------------------------
# 模块2 - 视频分析（调用 doubao-video-analyzer · 本地模式）
# ---------------------------------------------------------------------------

# 分析 prompt：要求模型以影视分镜师身份输出结构化 JSON
ANALYSIS_PROMPT = r"""### 角色
你是一位专业的影视分镜师和AI绘画提示词专家。

### 任务
仔细观看这段视频，识别每个关键场景/镜头切换。为每个场景输出以下信息。

### 要求
1. 按时间顺序逐个场景分析，不要遗漏任何镜头切换。
2. 每个场景的 `ai_prompt` 必须是**纯英文**，风格适合 Stable Diffusion / Midjourney 使用。
3. `ai_prompt` 应包含：主体描述、场景环境、光影氛围、色调、画面构图、艺术风格等关键词，用逗号分隔。
4. 严格按以下 JSON 格式输出，**不要**在 JSON 外添加任何多余文字。

### 输出格式
```json
{
  "title": "视频标题/主题概述",
  "total_duration": "视频总时长",
  "scenes": [
    {
      "scene_number": 1,
      "timestamp": "0:00-0:03",
      "shot_type": "远景/全景/中景/近景/特写",
      "camera_angle": "平拍/俯拍/仰拍/侧拍/航拍",
      "camera_move": "推/拉/摇/移/跟/升降/旋转/静止",
      "description": "画面内容的详细中文描述，包括人物动作、表情、环境细节",
      "characters": "出场人物描述（外貌/服装/动作），无人物则填'无'",
      "setting": "场景环境（室内/室外、具体地点、天气、时间等）",
      "mood": "氛围/情绪基调",
      "color_tone": "主色调/色彩风格",
      "sound": "音效/配乐/对白描述",
      "ai_prompt": "English AI painting prompt for this scene, detailed, comma-separated keywords"
    }
  ]
}
```"""


def _extract_text_from_response_repr(text):
    """
    从 volcenginesdkarkruntime Response 对象的 repr 字符串中提取实际文本内容。

    parse_video.py 直接 print(response)，输出的是 Response(...) 的 repr。
    实际内容在 ResponseOutputText(type='output_text', text='...') 中。
    """
    # 匹配 ResponseOutputText 中的 text 字段（最长匹配）
    m = re.search(r"ResponseOutputText\(type='output_text', text='(.*?)'(?:, annotations=)", text, re.DOTALL)
    if m:
        # repr 中的字符串用单引号包裹，内部的换行是 \n 字面量
        raw = m.group(1)
        # 处理 repr 转义：\n → 换行, \' → ', \\ → \
        raw = raw.replace('\\n', '\n').replace("\\'", "'").replace('\\\\', '\\')
        return raw
    return None


def parse_json_from_output(text):
    """
    从模型输出文本中提取 JSON 数据。

    支持以下情况：
    1. 输出本身就是纯 JSON
    2. JSON 被包裹在 ```json ... ``` 代码块中
    3. 输出是 volcenginesdkarkruntime Response 对象的 repr
    4. JSON 散落在其他文字中间
    """
    text = text.strip()

    # 尝试0: 如果是 Response(...) repr，先提取实际文本
    if text.startswith('Response('):
        extracted = _extract_text_from_response_repr(text)
        if extracted:
            text = extracted.strip()

    # 尝试1: 直接解析
    try:
        return json.loads(text)
    except json.JSONDecodeError:
        pass

    # 尝试2: 提取 ```json ... ``` 代码块
    m = re.search(r'```json\s*\n?(.*?)\n?\s*```', text, re.DOTALL)
    if m:
        try:
            return json.loads(m.group(1))
        except json.JSONDecodeError:
            pass

    # 尝试3: 找最外层的 { ... }（贪婪匹配）
    m = re.search(r'\{.*\}', text, re.DOTALL)
    if m:
        try:
            return json.loads(m.group(0))
        except json.JSONDecodeError:
            pass

    return None


def analyze_video(video_path):
    """
    调用 doubao-video-analyzer 分析视频（本地模式）。

    流程：
    1. 通过 subprocess 调用 parse_video.py
    2. 不加 --remote 标志 → 本地模式
    3. parse_video.py 内部通过 client.files.create() 上传视频到火山引擎
    4. 以 1fps 采样后交给 doubao-seed-2-0-pro 模型分析

    参数：
        video_path: 本地视频文件路径

    返回：
        dict - 包含 scenes 列表的分析结果
    """
    # 校验依赖
    script_path = _video_analyzer_script()
    if not os.path.isfile(script_path):
        raise FileNotFoundError(
            f'找不到 doubao-video-analyzer skill，请先安装: npx clawhub install doubao-video-analyzer'
        )

    if not os.environ.get('ARK_API_KEY'):
        raise EnvironmentError(
            '未设置 ARK_API_KEY 环境变量。\n'
            '请设置火山引擎 ARK API Key: set ARK_API_KEY=your_key'
        )

    video_path = os.path.abspath(video_path)
    if not os.path.isfile(video_path):
        raise FileNotFoundError(f'视频文件不存在: {video_path}')

    file_size_mb = os.path.getsize(video_path) / (1024 * 1024)
    print(f'[分析] 视频文件: {video_path} ({file_size_mb:.1f} MB)')
    print(f'[分析] 调用 doubao-video-analyzer (本地模式，1fps 采样) ...')
    print(f'[分析] 正在上传视频到火山引擎并等待处理，请耐心等待 ...')

    # 将 prompt 写入临时文件，避免 Windows 命令行编码问题
    import tempfile
    prompt_fd, prompt_path = tempfile.mkstemp(suffix='.txt', prefix='prompt_')
    try:
        with os.fdopen(prompt_fd, 'w', encoding='utf-8') as pf:
            pf.write(ANALYSIS_PROMPT)

        # 调用 parse_video.py —— 本地模式（不加 --remote）
        cmd = [
            sys.executable, script_path,
            '--video', video_path,
            '--prompt', ANALYSIS_PROMPT,
        ]

        env = os.environ.copy()
        env['PYTHONIOENCODING'] = 'utf-8'

        try:
            result = subprocess.run(
                cmd,
                capture_output=True,
                timeout=600,  # 10分钟超时（上传+处理+分析可能较慢）
                env=env,
            )
        except subprocess.TimeoutExpired:
            raise RuntimeError('视频分析超时（10分钟），视频可能过大，请尝试裁剪后重试')

        stdout_text = result.stdout.decode('utf-8', errors='replace')
        stderr_text = result.stderr.decode('utf-8', errors='replace')
    finally:
        os.unlink(prompt_path)

    # 输出调试日志
    if stderr_text.strip():
        for line in stderr_text.strip().splitlines():
            print(f'  [analyzer:err] {line}')

    if result.returncode != 0:
        error_msg = stderr_text.strip() or stdout_text.strip() or '未知错误'
        raise RuntimeError(f'doubao-video-analyzer 退出码 {result.returncode}: {error_msg}')

    if not stdout_text.strip():
        raise RuntimeError('doubao-video-analyzer 无输出，请检查 ARK_API_KEY 是否有效')

    # 解析 JSON 结果
    analysis = parse_json_from_output(stdout_text)
    if analysis is None:
        # 无法解析为 JSON，保存原始输出供调试
        print(f'[分析] 警告: 无法从模型输出中解析 JSON')
        print(f'[分析] 原始输出前500字符: {stdout_text[:500]}')
        # 返回包含原始文本的 fallback 结构
        return {
            'title': '（解析失败）',
            'total_duration': '未知',
            'scenes': [],
            '_raw_output': stdout_text,
        }

    # 校验基本结构
    if 'scenes' not in analysis:
        print(f'[分析] 警告: 模型输出缺少 scenes 字段')
        analysis['scenes'] = []

    scene_count = len(analysis.get('scenes', []))
    print(f'[分析] 完成! 共识别 {scene_count} 个场景/镜头')

    return analysis


def save_analysis(analysis, output_dir):
    """
    将分析结果保存为 JSON 文件。

    参数：
        analysis: 分析结果 dict
        output_dir: 输出目录

    返回：
        保存的文件路径
    """
    os.makedirs(output_dir, exist_ok=True)
    output_path = os.path.join(output_dir, 'analysis.json')

    with open(output_path, 'w', encoding='utf-8') as f:
        json.dump(analysis, f, ensure_ascii=False, indent=2)

    print(f'[输出] 分析结果已保存: {output_path}')
    return output_path


# ---------------------------------------------------------------------------
# 模块3 - 输出生成（分镜表格 + 提示词 + 游戏改写）
# ---------------------------------------------------------------------------

# 游戏/二次元风格追加关键词
GAME_STYLE_KEYWORDS = (
    'anime style, cel shading, game CG, visual novel, '
    'genshin impact style, vibrant colors, detailed illustration'
)

# ---------------------------------------------------------------------------
# 锈湖（Rusty Lake）风格改写 - 通过大模型改写
# ---------------------------------------------------------------------------

RUSTY_LAKE_MODEL = "ep-20260410110144-xxk6z"  # Seed-2.0-lite

RUSTY_LAKE_SYSTEM_PROMPT = """# Role：锈湖（Rusty Lake）风格资深分镜师 & AI 绘图提示词专家

## Task
请将我提供的"普通现实主义分镜"改写为"锈湖（Rusty Lake）游戏风格"的分镜。你需要修改【画面描述】以符合锈湖的诡异悬疑氛围，并重写对应的【英文绘图 Prompt】（适用于 Midjourney/Stable Diffusion）。

## 锈湖风格核心要素（Rusty Lake Aesthetic）
在改写时，请务必将以下元素巧妙地融入原本平淡的场景中：
1. **视觉基调**：2D平面手绘风格（2D illustration, vector art），复古色调（怀旧黄、暗红、阴冷蓝、灰褐），低饱和度，光影生硬且对比强烈。
2. **场景特征**：剥落的复古壁纸，破旧的木质家具，封闭的房间感（类似密室逃脱），墙上可能有奇怪的挂画、时钟或镜子。
3. **超现实/诡异元素**：黑方块/白方块（Black/White Cube）、黑影人（Corrupted Soul）、流血的细节、玻璃罐里的眼球/器官、长着动物头颅（乌鸦、猫头鹰、鹿、兔子）的人、悬浮的物体。
4. **镜头语言**：多采用固定机位（模拟点击解谜游戏的视角）、平视中心对称构图，缺乏景深（扁平化）。

## 改写规则
- 保持原分镜的基本动作和大致场景逻辑，但将其"锈湖化"（例如：现代超市冰柜变成复古生锈的冰箱，现代宿舍变成维多利亚式或70年代的诡异走廊）。
- 【画面描述】需要用中文生动描绘出诡异、惊悚、超现实的细节。
- 【英文 Prompt】必须包含关键风格词：`Rusty Lake game style, 2D flat illustration, surrealism, macabre, eerie atmosphere, vintage colors, point-and-click adventure game art --ar 16:9`

## 输出格式
对每个分镜，请严格按以下格式输出：

**画面描述**: （改写后的中文描述）

```
（改写后的英文绘图Prompt）
```

只输出改写后的内容，不要输出其他解释。"""


def _get_ark_client():
    """获取火山引擎 Ark 客户端（懒加载）"""
    from volcenginesdkarkruntime import Ark
    api_key = os.environ.get('ARK_API_KEY')
    if not api_key:
        raise EnvironmentError('未设置 ARK_API_KEY 环境变量')
    return Ark(base_url='https://ark.cn-beijing.volces.com/api/v3', api_key=api_key)


def _extract_llm_text(response):
    """从 Ark responses API 返回中提取文本"""
    # output 是 list，找 type='message' 的项
    for item in response.output:
        if item.type == 'message':
            for content in item.content:
                if content.type == 'output_text':
                    return content.text
    # fallback
    if response.text:
        return response.text
    return str(response.output)


def rewrite_scene_rusty_lake_llm(scene, client):
    """
    调用 Seed-2.0-lite 大模型将单个分镜改写为锈湖风格。

    参数：
        scene: 已规范化的 scene dict
        client: Ark 客户端实例

    返回：
        (new_description, new_prompt) 元组
    """
    shot_angle = _format_shot_angle(scene)
    user_input = f"""请将以下分镜改写为锈湖风格：

**景别**: {shot_angle}

**画面描述**: {scene.get('description', '')}

```
{scene.get('ai_prompt', '')}
```"""

    response = client.responses.create(
        model=RUSTY_LAKE_MODEL,
        input=[
            {"role": "system", "content": RUSTY_LAKE_SYSTEM_PROMPT},
            {"role": "user", "content": user_input},
        ],
    )

    result_text = _extract_llm_text(response)

    # 解析返回的 画面描述 和 英文 prompt
    desc_match = re.search(r'\*\*画面描述\*\*:\s*(.+?)(?:\n\n|\n```)', result_text, re.DOTALL)
    prompt_match = re.search(r'```\n?(.+?)\n?```', result_text, re.DOTALL)

    new_desc = desc_match.group(1).strip() if desc_match else result_text.strip()
    new_prompt = prompt_match.group(1).strip() if prompt_match else scene.get('ai_prompt', '')

    return new_desc, new_prompt


def rewrite_analysis_rusty_lake(analysis):
    """
    使用大模型将整个分析结果改写为锈湖风格。

    参数：
        analysis: 原始分析结果 dict

    返回：
        新的分析结果 dict（锈湖风格）
    """
    import time

    client = _get_ark_client()
    scenes = analysis.get('scenes', [])

    rusty_analysis = dict(analysis)
    rusty_analysis['title'] = f'{analysis.get("title", "")}（锈湖风格改写）'
    rusty_scenes = []

    for i, s in enumerate(scenes):
        s = _normalize_scene(s)
        print(f'  [锈湖改写] Scene {i + 1}/{len(scenes)} ...')
        try:
            new_desc, new_prompt = rewrite_scene_rusty_lake_llm(s, client)
            rusty_scene = dict(s)
            rusty_scene['description'] = new_desc
            rusty_scene['ai_prompt'] = new_prompt
            rusty_scenes.append(rusty_scene)
        except Exception as e:
            print(f'  [锈湖改写] Scene {i + 1} 失败: {e}，使用原始内容')
            rusty_scenes.append(dict(s))
        # 避免请求过快
        if i < len(scenes) - 1:
            time.sleep(1)

    rusty_analysis['scenes'] = rusty_scenes
    return rusty_analysis


def _normalize_scene(scene):
    """
    将分析结果中的单个 scene dict 规范化，补全缺失字段。

    分析模型输出的字段可能不完整，这里确保每个字段都有默认值。
    """
    defaults = {
        'scene_number': 0,
        'timestamp': '',
        'shot_type': '中景',
        'camera_angle': '平拍',
        'camera_move': '静止',
        'description': '',
        'characters': '无',
        'setting': '',
        'mood': '',
        'color_tone': '',
        'sound': '',
        'ai_prompt': '',
    }
    normalized = {}
    for key, default in defaults.items():
        normalized[key] = scene.get(key, default) or default
    return normalized


def _format_shot_angle(scene):
    """
    将景别、角度、运镜合并为一列文本，格式参考 script-to-storyboard 示例。

    例如: "中景/平拍/推镜头"、"特写/俯拍"（运镜为"静止"时省略）。
    """
    shot_type = scene.get('shot_type', '中景')
    angle = scene.get('camera_angle', '平拍')
    move = scene.get('camera_move', '静止')

    if move and move != '静止':
        return f'{shot_type}/{angle}/{move}'
    return f'{shot_type}/{angle}'


# ---- 分镜表格 (Markdown) ------------------------------------------------

def generate_storyboard_md(analysis, output_path):
    """
    生成 Markdown 格式的分镜表格。

    表格列与 script-to-storyboard/references/示例分镜.md 保持一致：
    镜号 | 景别/拍摄角度 | 画面内容 | 出场人物 | 场景 | 音效

    参数：
        analysis:    分析结果 dict（含 scenes 列表）
        output_path: 输出 .md 文件路径

    返回：
        output_path
    """
    scenes = analysis.get('scenes', [])
    title = analysis.get('title', '分镜脚本')

    lines = [
        f'# {title}',
        '',
        f'> 总时长: {analysis.get("total_duration", "未知")}',
        '',
        '| 镜号 | 景别/拍摄角度 | 画面内容 | 出场人物 | 场景 | 音效 |',
        '|------|--------------|----------|---------|------|------|',
    ]

    for s in scenes:
        s = _normalize_scene(s)
        shot_angle = _format_shot_angle(s)
        # 转义 Markdown 表格中的竖线
        desc = str(s['description']).replace('|', '\\|')
        chars = str(s['characters']).replace('|', '\\|')
        setting = str(s['setting']).replace('|', '\\|')
        sound = str(s['sound']).replace('|', '\\|')

        lines.append(
            f'| {s["scene_number"]} | {shot_angle} | {desc} | {chars} | {setting} | {sound} |'
        )

    lines.append('')  # trailing newline

    os.makedirs(os.path.dirname(output_path) or '.', exist_ok=True)
    with open(output_path, 'w', encoding='utf-8') as f:
        f.write('\n'.join(lines))

    print(f'[输出] 分镜表格 (Markdown): {output_path}')
    return output_path


# ---- 分镜表格 (CSV) ------------------------------------------------------

def generate_storyboard_csv(analysis, output_path):
    """
    生成 CSV 格式的分镜表格。

    列定义与 script-to-storyboard/scripts/convert.py 的 generate_csv() 一致：
    镜号, 景别/拍摄角度, 画面内容, 出场人物, 场景, 音效

    使用 utf-8-sig 编码以兼容 Excel 直接打开。

    参数：
        analysis:    分析结果 dict（含 scenes 列表）
        output_path: 输出 .csv 文件路径

    返回：
        output_path
    """
    scenes = analysis.get('scenes', [])
    fieldnames = ['镜号', '景别/拍摄角度', '画面内容', '出场人物', '场景', '音效']

    os.makedirs(os.path.dirname(output_path) or '.', exist_ok=True)
    with open(output_path, 'w', newline='', encoding='utf-8-sig') as f:
        writer = csv.DictWriter(f, fieldnames=fieldnames)
        writer.writeheader()

        for s in scenes:
            s = _normalize_scene(s)
            writer.writerow({
                '镜号': s['scene_number'],
                '景别/拍摄角度': _format_shot_angle(s),
                '画面内容': s['description'],
                '出场人物': s['characters'],
                '场景': s['setting'],
                '音效': s['sound'],
            })

    print(f'[输出] 分镜表格 (CSV): {output_path}')
    return output_path


# ---- AI 绘画提示词 -------------------------------------------------------

def generate_prompts_md(analysis, output_path, *, style_suffix=None):
    """
    生成 AI 绘画提示词文件（每个场景一条英文 prompt）。

    参数：
        analysis:     分析结果 dict
        output_path:  输出 .md 文件路径
        style_suffix: 可选的风格后缀，如游戏风格关键词，会追加到每条 prompt 末尾

    返回：
        output_path
    """
    scenes = analysis.get('scenes', [])
    title = analysis.get('title', 'AI Painting Prompts')
    suffix_label = '（游戏/二次元风格改写）' if style_suffix else '（原始反推）'

    lines = [
        f'# AI 绘画提示词 {suffix_label}',
        '',
        f'> 来源: {title}',
        '',
    ]

    for s in scenes:
        s = _normalize_scene(s)
        prompt = s['ai_prompt']

        # 追加风格后缀
        if style_suffix and prompt:
            prompt = f'{prompt}, {style_suffix}'

        lines.append(f'## Scene {s["scene_number"]}  [{s["timestamp"]}]')
        lines.append('')
        lines.append(f'**景别**: {_format_shot_angle(s)}')
        lines.append('')
        lines.append(f'**画面描述**: {s["description"]}')
        lines.append('')
        lines.append(f'```')
        lines.append(prompt)
        lines.append(f'```')
        lines.append('')

    os.makedirs(os.path.dirname(output_path) or '.', exist_ok=True)
    with open(output_path, 'w', encoding='utf-8') as f:
        f.write('\n'.join(lines))

    print(f'[输出] AI 提示词: {output_path}')
    return output_path


# ---- 游戏向改写 -----------------------------------------------------------

def rewrite_scene_for_game(scene):
    """
    将单个场景改写为游戏/二次元/动漫风格。

    改写规则：
    1. ai_prompt 末尾追加 GAME_STYLE_KEYWORDS
    2. description 中的环境描述添加游戏风格修饰
    3. mood / color_tone 向二次元风格偏移

    参数：
        scene: 已规范化的 scene dict

    返回：
        新的 scene dict（深拷贝，不修改原始数据）
    """
    game_scene = dict(scene)  # shallow copy is enough for string values

    # 改写 ai_prompt
    original_prompt = game_scene.get('ai_prompt', '')
    if original_prompt:
        game_scene['ai_prompt'] = f'{original_prompt}, {GAME_STYLE_KEYWORDS}'
    else:
        game_scene['ai_prompt'] = GAME_STYLE_KEYWORDS

    # 改写 description —— 追加游戏风格修饰
    desc = game_scene.get('description', '')
    if desc:
        game_scene['description'] = f'{desc}（游戏CG风格，动漫渲染）'

    # 改写 mood
    mood = game_scene.get('mood', '')
    if mood:
        game_scene['mood'] = f'{mood}，二次元风格'

    # 改写 color_tone
    color_tone = game_scene.get('color_tone', '')
    if color_tone:
        game_scene['color_tone'] = f'{color_tone}，高饱和动漫色彩'

    return game_scene


def rewrite_analysis_for_game(analysis):
    """
    将整个分析结果改写为游戏/二次元风格。

    参数：
        analysis: 原始分析结果 dict

    返回：
        新的分析结果 dict（游戏风格）
    """
    game_analysis = dict(analysis)
    game_analysis['title'] = f'{analysis.get("title", "")}（游戏向改写）'
    game_analysis['scenes'] = [
        rewrite_scene_for_game(_normalize_scene(s))
        for s in analysis.get('scenes', [])
    ]
    return game_analysis


# ---- 输出主编排 -----------------------------------------------------------

def generate_outputs(analysis, output_dir, *, no_rewrite=False, rusty_lake=False):
    """
    模块3 主编排函数：从分析结果生成所有输出文件。

    输出文件列表：
        output/
        ├── analysis.json              # （已在 save_analysis 中生成）
        ├── original_prompts.md        # 原始反推提示词
        ├── original_storyboard.md     # 原始分镜表格（Markdown）
        ├── original_storyboard.csv    # 原始分镜表格（CSV）
        ├── game_prompts.md            # 游戏/二次元风改写提示词
        ├── game_storyboard.md         # 游戏向分镜表格（Markdown）
        ├── game_storyboard.csv        # 游戏向分镜表格（CSV）
        ├── rusty_lake_prompts.md      # 锈湖风格改写提示词（大模型）
        ├── rusty_lake_storyboard.md   # 锈湖风格分镜表格（Markdown）
        └── rusty_lake_storyboard.csv  # 锈湖风格分镜表格（CSV）

    参数：
        analysis:   分析结果 dict（含 scenes 列表）
        output_dir: 输出目录路径
        no_rewrite: 是否跳过游戏向改写（默认 False）
        rusty_lake: 是否启用锈湖风格大模型改写（默认 False）

    返回：
        生成的文件路径列表
    """
    scenes = analysis.get('scenes', [])
    if not scenes:
        print('[输出] 警告: 没有场景数据，无法生成输出文件')
        if analysis.get('_raw_output'):
            # 保存原始文本以便人工检查
            raw_path = os.path.join(output_dir, 'raw_output.txt')
            with open(raw_path, 'w', encoding='utf-8') as f:
                f.write(analysis['_raw_output'])
            print(f'[输出] 原始模型输出已保存: {raw_path}')
        return []

    os.makedirs(output_dir, exist_ok=True)
    generated = []

    print(f'\n{"="*60}')
    print(f'开始生成输出文件（共 {len(scenes)} 个场景）...')
    print(f'{"="*60}\n')

    # --- 原始版本 ---
    generated.append(
        generate_storyboard_md(analysis, os.path.join(output_dir, 'original_storyboard.md'))
    )
    generated.append(
        generate_storyboard_csv(analysis, os.path.join(output_dir, 'original_storyboard.csv'))
    )
    generated.append(
        generate_prompts_md(analysis, os.path.join(output_dir, 'original_prompts.md'))
    )

    # --- 游戏向改写（简单关键词追加） ---
    if not no_rewrite:
        game_analysis = rewrite_analysis_for_game(analysis)
        generated.append(
            generate_storyboard_md(game_analysis, os.path.join(output_dir, 'game_storyboard.md'))
        )
        generated.append(
            generate_storyboard_csv(game_analysis, os.path.join(output_dir, 'game_storyboard.csv'))
        )
        generated.append(
            generate_prompts_md(
                game_analysis,
                os.path.join(output_dir, 'game_prompts.md'),
                style_suffix=GAME_STYLE_KEYWORDS,
            )
        )

    # --- 锈湖风格改写（大模型改写） ---
    if rusty_lake:
        print(f'\n{"="*60}')
        print(f'开始锈湖（Rusty Lake）风格改写（调用 Seed-2.0-lite）...')
        print(f'{"="*60}\n')
        try:
            rusty_analysis = rewrite_analysis_rusty_lake(analysis)
            generated.append(
                generate_storyboard_md(rusty_analysis, os.path.join(output_dir, 'rusty_lake_storyboard.md'))
            )
            generated.append(
                generate_storyboard_csv(rusty_analysis, os.path.join(output_dir, 'rusty_lake_storyboard.csv'))
            )
            generated.append(
                generate_prompts_md(rusty_analysis, os.path.join(output_dir, 'rusty_lake_prompts.md'))
            )
        except Exception as e:
            print(f'[锈湖改写] 失败: {e}')

    print(f'\n[输出] 全部完成! 共生成 {len(generated)} 个文件:')
    for path in generated:
        print(f'  - {path}')

    return generated


# ---------------------------------------------------------------------------
# CLI 入口
# ---------------------------------------------------------------------------

def build_parser():
    parser = argparse.ArgumentParser(
        description='从视频反推AI绘画提示词和分镜脚本',
        formatter_class=argparse.RawDescriptionHelpFormatter,
        epilog=__doc__,
    )
    parser.add_argument('url', nargs='?', default=None,
                        help='视频页面URL（抖音 / YouTube / B站 等）')
    parser.add_argument('--local', type=str, default=None,
                        help='直接分析本地视频文件（跳过下载）')
    parser.add_argument('--output', '-o', type=str, default=None,
                        help='输出目录（默认: ./output）')
    parser.add_argument('--resolution', '-r', type=str, default='1080p',
                        help='下载分辨率（默认: 1080p）')
    parser.add_argument('--download-only', action='store_true',
                        help='仅下载视频，不进行分析')
    parser.add_argument('--no-rewrite', action='store_true',
                        help='跳过游戏向改写')
    parser.add_argument('--rusty-lake', action='store_true',
                        help='启用锈湖（Rusty Lake）风格大模型改写（需要 ARK_API_KEY）')
    return parser


def main():
    parser = build_parser()
    args = parser.parse_args()

    # 参数校验
    if not args.url and not args.local:
        parser.print_help()
        print('\n错误: 请提供视频URL 或使用 --local 指定本地视频文件')
        sys.exit(1)

    # 确定输出目录
    output_dir = args.output or os.path.join('.', 'output')
    os.makedirs(output_dir, exist_ok=True)
    video_dir = os.path.join(output_dir, 'video')
    os.makedirs(video_dir, exist_ok=True)

    # ------------------------------------------------------------------
    # Step 1: 获取视频文件路径
    # ------------------------------------------------------------------
    if args.local:
        # 本地模式：直接使用用户提供的文件
        video_path = os.path.abspath(args.local)
        if not os.path.isfile(video_path):
            print(f'错误: 找不到本地视频文件: {video_path}')
            sys.exit(1)
        print(f'[本地] 使用本地视频: {video_path}')
    else:
        # 在线模式：调用 video-downloader 下载
        try:
            video_path = download_video(args.url, video_dir, args.resolution)
        except Exception as e:
            print(f'错误: 视频下载失败 - {e}')
            sys.exit(1)

    if args.download_only:
        print(f'\n下载完成，视频文件: {video_path}')
        print('（已指定 --download-only，跳过分析步骤）')
        sys.exit(0)

    # ------------------------------------------------------------------
    # Step 2: 视频分析（模块2 - 调用 doubao-video-analyzer）
    # ------------------------------------------------------------------
    print(f'\n{"="*60}')
    print(f'视频已就绪: {video_path}')
    print(f'开始视频分析 ...')
    print(f'{"="*60}\n')

    try:
        analysis = analyze_video(video_path)
    except Exception as e:
        print(f'错误: 视频分析失败 - {e}')
        sys.exit(1)

    # 保存分析结果 JSON
    save_analysis(analysis, output_dir)

    # ------------------------------------------------------------------
    # Step 3: 输出生成（模块3 - 分镜表格 + 提示词 + 游戏改写）
    # ------------------------------------------------------------------
    generated = generate_outputs(analysis, output_dir, no_rewrite=args.no_rewrite, rusty_lake=args.rusty_lake)

    if generated:
        print(f'\n{"="*60}')
        print(f'全部流程完成!')
        print(f'输出目录: {os.path.abspath(output_dir)}')
        print(f'{"="*60}')
    else:
        print('\n警告: 未生成任何输出文件，请检查分析结果')


if __name__ == '__main__':
    main()
