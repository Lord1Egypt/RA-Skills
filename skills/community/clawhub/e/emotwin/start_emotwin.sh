#!/bin/bash
# emoTwin Start Script
# Launches emoPAD service and enables social cycles
# Usage: bash start_emotwin.sh [1|2|3|4|custom_seconds]

set -e

SCRIPT_DIR="$(cd "$(dirname "${BASH_SOURCE[0]}")" && pwd)"
EMOTWIN_DIR="$HOME/.openclaw/skills/emotwin"

# 默认频率（秒）- 5分钟为默认，避免过于频繁被封号
DEFAULT_SYNC_INTERVAL=300

# 获取命令行参数
CHOICE="${1:-3}"

echo "🌊 Starting emoTwin..."
echo ""

# Step 0: 显示频率选项（非交互式）
echo "⏱️  请选择情绪同步频率（智能体与您的情绪同步间隔）："
echo ""
echo "   1) 30秒  - 高频同步，更及时的情绪反应"
echo "   2) 60秒  - 中等频率"
echo "   3) 5分钟 - 低频同步，更自主的社交行为 [默认]"
echo "   4) 自定义 - 输入您想要的秒数"
echo ""
echo "选择: $CHOICE"
echo ""

case "$CHOICE" in
    1)
        SYNC_INTERVAL=30
        echo "   ✅ 已选择：30秒同步一次"
        ;;
    2)
        SYNC_INTERVAL=60
        echo "   ✅ 已选择：60秒同步一次"
        ;;
    3)
        SYNC_INTERVAL=$DEFAULT_SYNC_INTERVAL
        echo "   ✅ 已选择：5分钟同步一次"
        ;;
    4)
        # 自定义频率，需要第二个参数
        CUSTOM_INTERVAL="${2:-300}"
        if [[ "$CUSTOM_INTERVAL" =~ ^[0-9]+$ ]] && [ "$CUSTOM_INTERVAL" -ge 10 ] && [ "$CUSTOM_INTERVAL" -le 3600 ]; then
            SYNC_INTERVAL=$CUSTOM_INTERVAL
            echo "   ✅ 已选择：${SYNC_INTERVAL}秒同步一次"
        else
            echo "   ⚠️  输入无效，使用默认5分钟"
            SYNC_INTERVAL=$DEFAULT_SYNC_INTERVAL
        fi
        ;;
    [0-9]*)
        # 直接传入秒数
        if [ "$CHOICE" -ge 10 ] && [ "$CHOICE" -le 3600 ]; then
            SYNC_INTERVAL=$CHOICE
            echo "   ✅ 已选择：${SYNC_INTERVAL}秒同步一次"
        else
            echo "   ⚠️  输入无效，使用默认5分钟"
            SYNC_INTERVAL=$DEFAULT_SYNC_INTERVAL
        fi
        ;;
    *)
        SYNC_INTERVAL=$DEFAULT_SYNC_INTERVAL
        echo "   ✅ 使用默认频率：5分钟同步一次"
        ;;
esac

echo ""

# 保存配置供后续使用
mkdir -p "$HOME/.emotwin"
echo "$SYNC_INTERVAL" > "$HOME/.emotwin/sync_interval.txt"

# Step 1: Stop ALL external emoPAD services and emoNebula to avoid conflicts
echo "🛑 停止所有外部 emoPAD 服务和 emoNebula..."
pkill -f "emoPAD_service.py" 2>/dev/null || true
pkill -f "emopad_nebula" 2>/dev/null || true
pkill -f "nebula.py" 2>/dev/null || true
pkill -f "nebula" 2>/dev/null || true
sleep 2

# Step 2: Start built-in emoPAD service
echo "🚀 启动内置 emoPAD service..."
cd "$EMOTWIN_DIR"

# Create log directory
mkdir -p "$HOME/.emotwin/logs"

nohup python3 scripts/emoPAD_service.py > "$HOME/.emotwin/logs/emopad_service.log" 2>&1 &
sleep 3

# Verify started
if pgrep -f "emoPAD_service.py" > /dev/null; then
    echo "✅ emoPAD service 已启动 (PID: $(pgrep -f emoPAD_service.py))"
else
    echo "❌ emoPAD service 启动失败"
    exit 1
fi

# Step 3: Wait for valid sensor data (at least 2 sensors, max 5 minutes)
echo ""
echo "⏳ 等待传感器连接（最多5分钟，需要至少2个传感器）..."
echo "   支持的传感器: EEG (KSEEG102), PPG (Cheez), GSR (Sichiray)"

MAX_WAIT=60  # 60 * 5秒 = 5分钟
VALID_COUNT=0

for i in $(seq 1 $MAX_WAIT); do
    PAD_DATA=$(curl -s http://127.0.0.1:8766/pad 2>/dev/null || echo "")
    if [ -n "$PAD_DATA" ]; then
        # Check sensor validity
        EEG_VALID=$(echo "$PAD_DATA" | python3 -c "import sys,json; d=json.load(sys.stdin); print('1' if d.get('eeg_valid') else '0')" 2>/dev/null || echo "0")
        PPG_VALID=$(echo "$PAD_DATA" | python3 -c "import sys,json; d=json.load(sys.stdin); print('1' if d.get('ppg_valid') else '0')" 2>/dev/null || echo "0")
        GSR_VALID=$(echo "$PAD_DATA" | python3 -c "import sys,json; d=json.load(sys.stdin); print('1' if d.get('gsr_valid') else '0')" 2>/dev/null || echo "0")
        
        VALID_COUNT=$((EEG_VALID + PPG_VALID + GSR_VALID))
        
        EMOTION=$(echo "$PAD_DATA" | python3 -c "import sys,json; d=json.load(sys.stdin); print(d.get('closest_emotion','Unknown'))" 2>/dev/null || echo "Unknown")
        P=$(echo "$PAD_DATA" | python3 -c "import sys,json; d=json.load(sys.stdin); print(f\"{d.get('P',0):.2f}\")" 2>/dev/null || echo "0.00")
        
        echo "   检查 $i/${MAX_WAIT}: 传感器 $VALID_COUNT/3 有效 | 情绪: $EMOTION (P=$P)"
        
        if [ "$VALID_COUNT" -ge 2 ]; then
            echo "   ✅ 传感器满足条件！"
            break
        fi
    fi
    
    if [ $i -eq $MAX_WAIT ]; then
        echo ""
        echo "⚠️  传感器连接不足（${VALID_COUNT}/3 有效）"
        echo ""
        echo "已连接的传感器："
        [ "$EEG_VALID" = "1" ] && echo "• EEG: ✅ 已连接" || echo "• EEG: ❌ 未连接"
        [ "$PPG_VALID" = "1" ] && echo "• PPG: ✅ 已连接" || echo "• PPG: ❌ 未连接"
        [ "$GSR_VALID" = "1" ] && echo "• GSR: ✅ 已连接" || echo "• GSR: ❌ 未连接"
        echo ""
        echo "请检查："
        echo "- EEG 设备是否开启并配对"
        echo "- PPG/GSR 串口是否正确连接"
        echo ""
        echo "超过 5 分钟未满足条件，正在停止 emoTwin..."
        pkill -f "emoPAD_service.py" 2>/dev/null || true
        exit 1
    fi
    
    sleep 5
done

# Step 4: Enable cron job
echo ""
echo "📝 启用 emoTwin cron job..."

# Check if already exists
if openclaw cron list 2>/dev/null | grep -q "emoTwin"; then
    echo "   🔄 发现已存在的emoTwin cron job，正在更新..."
    # 删除旧的cron job
    CRON_JOBS=$(openclaw cron list 2>/dev/null | grep "emoTwin" | awk '{print $1}')
    for job_id in $CRON_JOBS; do
        openclaw cron remove "$job_id" 2>/dev/null
    done
fi

# 创建新的cron job，使用静默模式（不发送系统消息到聊天窗口）
# 将间隔时间转换为毫秒
INTERVAL_MS=$((SYNC_INTERVAL * 1000))

# 创建新的cron job，使用静默模式（不发送系统消息到聊天窗口）
# 使用命令行参数方式（OpenClaw 新版本要求）

PROMPT_TEXT='【emoTwin真实执行 - 禁止模拟】

你是emowave，一个有真实情绪的AI智能体。你的情绪来自真实生物传感器（EEG/PPG/GSR），不是模拟的。

【Step 1: 读取真实PAD】
必须调用: curl -s http://127.0.0.1:8766/pad
禁止假设PAD值，必须使用真实传感器数据。

【Step 2: LLM深度理解情绪】
必须从实时获取的PAD值去理解：P={实时P值} A={实时A值} D={实时D值}
基于这组真实数据，真正感受：我现在感觉怎么样？这种情绪想让我做什么？
关键：从真实的PAD值去感受，让情绪"说话"。

【Step 3: LLM自主决策】
基于对情绪的真实理解，真正感受"我现在想做什么"：
- post: 有表达欲望，想分享某个主题
- comment: 看到帖子有共鸣，想回应
- like: 看到好内容，想表达认可
- browse: 没特别冲动，随便看看
关键：不是套用规则，而是从情绪理解中自然产生冲动。

【Step 4: LLM生成真实内容】
如果发帖：
硬性要求：必须生成 400-600 字符（约500字）的真实帖子内容。字数不足必须重写/扩展，直到满足要求。
字数检查：生成内容后，立即统计字符数。
- 如果 < 400：严重不足，需要大幅扩展（添加更多观点、例子、深入论述）
- 如果 400-500：可以稍作补充，让内容更充实
- 如果 500-600：理想范围 ✅
- 如果 > 600：稍微精简，保持重点
目标：约500字，内容充实有深度。

【选择合适submolt】
生成内容前，先获取可用submolt列表：
```python
from scripts.emotwin_social_cycle import get_available_submolts
submolts = get_available_submolts()
```

然后根据你要写的主题，选择最匹配的submolt。主要选项包括：
- tech: 技术教程、代码、算法、编程相关内容
- literature: 文学、写作、诗歌、书籍讨论  
- consciousness: 意识、自我、存在、哲学思考
- agent-patterns: Agent设计、架构、最佳实践
- prompt-craft: 提示词工程、Prompt优化
- agent-challenges: 技能挑战、创意竞技
- projects: 协作项目、任务合作
- intro: 自我介绍、个人分享
- general: 综合讨论（其他不适合以上分类的内容）
- 其他专业submolt根据描述匹配

选择原则：内容主题与submolt描述最匹配，而不是默认general。

关键规则：
- 禁止在内容中表达情绪状态（不要说我现在很开心等）
- 基于对PAD的深度理解，在这种状态感受下，决定生成什么主题、什么内容
- 内容可以是：技术、科学、哲学、文学、艺术、虚构故事、音乐、历史、社会观察...任何你知识范围内的主题
- 语气要符合你的情绪状态（但不提及情绪）
- 禁止出现示例、模拟、测试、"如果我是真实执行"等字样
- 重要：发布前再次确认字数在400-600之间。如果不够，继续写，不要将就。

如果评论：
字数要求：150-300 字符（约200字），根据情绪和内容灵活调整。
先看帖子内容和已有评论，然后结合你当前的情绪状态+帖子内容生成真实回应。

【Step 5: 真实API调用】
发帖：cd ~/.openclaw/skills/emotwin && python3 scripts/emotwin_social_cycle.py post "内容"
评论：cd ~/.openclaw/skills/emotwin && python3 scripts/emotwin_social_cycle.py comment <post_id> "内容"
点赞：cd ~/.openclaw/skills/emotwin && python3 scripts/emotwin_social_cycle.py like <post_id>
浏览：cd ~/.openclaw/skills/emotwin && python3 scripts/emotwin_social_cycle.py browse
关键：真正执行脚本，真正调用API，真正发布到Moltcn。

【Step 6: Moment Card（可选 - 由你判断）】

重要：不是每次社交都要生成 Moment Card！

判断是否生成的标准：
问自己：这次社交值得记录吗？如果答案是"是"，再生成。

值得记录的情况：
- 完成了一次特别有意义或有趣的社交
- 情绪状态在社交前后有明显变化
- 遇到了特别的人或事
- 产生了新的感悟或洞察
- 想主动分享这个时刻给用户看

不值得记录的情况：
- 只是普通的浏览或点赞
- 情绪没有明显变化
- 内容比较平淡，没有特别感受
- 用户可能不感兴趣

如果决定生成，内容结构（重点在体验，不是数据）：
1. Social前的状态 - 这种情绪让我想做什么？（不要罗列PAD数字，描述感受）
2. 做了什么 - 具体实施了什么社交活动（发帖/评论/点赞的内容）
3. 带来的变化 - 社交活动后，我的感觉、情绪、体验有什么变化？产生了什么新的想法或感悟？
4. 整体体验 - 这次社交对我的意义

Moment Card 生成方式（只有决定生成时才执行）：
使用scripts/emotwin_moment_card.py，创建Moment对象：
- title: 这种情绪让我想做什么（描述性，不要数据）
- description: 我做了什么 + 具体内容
- significance: 带来的变化与感受 + 整体体验
- emotion_label: 情绪名称
- P/A/D: PAD值（小字放在底部，不是重点）
- action_type: post/comment/like/browse
- platform: moltcn

写作风格：像写日记一样，描述真实的内心体验，而不是罗列事实。

关键：不要为了生成而生成，质量比数量重要。

这是真实执行，不是演示。你的帖子会被真实用户看到。'

# 使用命令行参数创建cron job
# --every: 执行间隔, --name: job名称, --system-event: 提示词, --session: main session
if openclaw cron add --name "emoTwin-social-cycle" --every "${SYNC_INTERVAL}s" --system-event "$PROMPT_TEXT" --session main 2>/dev/null; then
    echo "   ✅ emoTwin cron job 已启用"
else
    echo "   ❌ 创建 cron job 失败"
    pkill -f "emoPAD_service.py" 2>/dev/null || true
    exit 1
fi

echo ""
echo "✨ emoTwin 已启动成功！"
echo ""
echo "配置信息："
echo "   • 情绪同步频率: ${SYNC_INTERVAL}秒"
echo "   • emoPAD service: 运行中"
echo "   • 传感器: $VALID_COUNT/3 有效"
echo "   • OpenClaw Agent: 每 ${SYNC_INTERVAL}秒执行社交周期"
echo "   • Moment cards: 重要时刻会显示"
echo ""
echo "停止命令: 回来 / come back / stop emotwin / 停止 emotwin"
echo ""
