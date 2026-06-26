#!/bin/bash
# intro-outro-generator.sh - 片头片尾模板生成
# 预设多种动画模板，支持自定义 logo、频道名、社交媒体链接
#
# 使用方式:
#   bash intro-outro-generator.sh --type intro --template fade --title "我的频道" --output intro.mp4
#   bash intro-outro-generator.sh --type outro --template social --title "感谢观看" --subtitle "记得三连！"

set -euo pipefail

source "$(dirname "$0")/colors.sh" 2>/dev/null || {
    RED='\033[0;31m'; GREEN='\033[0;32m'; YELLOW='\033[1;33m'
    BLUE='\033[0;34m'; NC='\033[0m'
}

TYPE="intro"         # intro | outro
TEMPLATE="fade"      # fade | zoom | slide | minimal | social | subscribe
TITLE=""
SUBTITLE=""
LOGO=""
DURATION=5
OUTPUT=""
BG_COLOR="black"
TEXT_COLOR="white"
ACCENT_COLOR="#FF6B35"
WIDTH=1920
HEIGHT=1080
FONT="PingFang SC"
FONT_SIZE_TITLE=80
FONT_SIZE_SUB=40
SOCIAL_LINKS=""

usage() {
    cat << 'EOF'
用法：intro-outro-generator.sh [选项]

必需:
  --title             标题文字 (频道名/视频标题)

可选:
  --type              类型：intro (片头) / outro (片尾) (默认：intro)
  --template, -t      模板 (见下方列表)
  --subtitle          副标题
  --logo              Logo 图片路径 (PNG/JPG)
  --duration, -d      时长秒数 (默认：5)
  --output, -o        输出文件 (默认：intro.mp4 / outro.mp4)
  --bg-color          背景色 (默认：black)
  --text-color        文字色 (默认：white)
  --accent            强调色 (默认：#FF6B35)
  --resolution        分辨率 WxH (默认：1920x1080)
  --social            社交媒体链接 (用于 social 模板)
  --font              字体 (默认：PingFang SC)
  --help              显示帮助

模板:
  fade        淡入淡出 (经典)
  zoom        缩放进入
  slide       从左滑入
  minimal     极简白底
  social      社交媒体卡片 (片尾推荐)
  subscribe   订阅提示 (片尾推荐)

示例:
  # 经典片头
  intro-outro-generator.sh --title "科技前沿" --subtitle "每周更新" --type intro -t fade

  # 社交媒体片尾
  intro-outro-generator.sh --title "感谢观看" --type outro -t social \
      --social "B站: @mychannel | 微博: @mychannel"

  # 带 Logo 的极简片头
  intro-outro-generator.sh --title "MyBrand" --logo ./logo.png -t minimal
EOF
    exit 0
}

while [[ $# -gt 0 ]]; do
    case $1 in
        --type) TYPE="$2"; shift 2 ;;
        --template|-t) TEMPLATE="$2"; shift 2 ;;
        --title) TITLE="$2"; shift 2 ;;
        --subtitle) SUBTITLE="$2"; shift 2 ;;
        --logo) LOGO="$2"; shift 2 ;;
        --duration|-d) DURATION="$2"; shift 2 ;;
        --output|-o) OUTPUT="$2"; shift 2 ;;
        --bg-color) BG_COLOR="$2"; shift 2 ;;
        --text-color) TEXT_COLOR="$2"; shift 2 ;;
        --accent) ACCENT_COLOR="$2"; shift 2 ;;
        --resolution) WIDTH=$(echo "$2" | cut -dx -f1); HEIGHT=$(echo "$2" | cut -dx -f2); shift 2 ;;
        --social) SOCIAL_LINKS="$2"; shift 2 ;;
        --font) FONT="$2"; shift 2 ;;
        --help|-h) usage ;;
        *) echo "未知参数：$1"; usage ;;
    esac
done

if [[ -z "$TITLE" ]]; then
    echo -e "${RED}❌ 必须提供 --title${NC}"
    usage
fi

[[ -z "$OUTPUT" ]] && OUTPUT="${TYPE}.mp4"

echo -e "${BLUE}🎬 ${TYPE} 生成器${NC}"
echo -e "标题：${GREEN}$TITLE${NC}"
[[ -n "$SUBTITLE" ]] && echo -e "副标题：${GREEN}$SUBTITLE${NC}"
echo -e "模板：${GREEN}$TEMPLATE${NC}"
echo -e "时长：${GREEN}${DURATION}s${NC}"
echo -e "分辨率：${GREEN}${WIDTH}x${HEIGHT}${NC}"
echo ""

# === 构建 ffmpeg 滤镜 ===
FADE_IN_DUR=1
FADE_OUT_DUR=1
HOLD_DUR=$((DURATION - FADE_IN_DUR - FADE_OUT_DUR))
[[ $HOLD_DUR -lt 1 ]] && HOLD_DUR=1

# 文字 Y 坐标
TITLE_Y="(h-text_h)/2"
SUB_Y="(h-text_h)/2+80"

case "$TEMPLATE" in
    fade)
        # 淡入停留淡出
        VF="color=c=${BG_COLOR}:s=${WIDTH}x${HEIGHT}:d=${DURATION},format=yuv420p"
        VF="${VF},drawtext=text='${TITLE}':fontfile=/System/Library/Fonts/PingFang.ttc:fontsize=${FONT_SIZE_TITLE}:fontcolor=${TEXT_COLOR}:x=(w-text_w)/2:y=${TITLE_Y}:alpha='if(lt(t,${FADE_IN_DUR}),t/${FADE_IN_DUR},if(gt(t,${DURATION}-${FADE_OUT_DUR}),(${DURATION}-t)/${FADE_OUT_DUR},1))'"
        if [[ -n "$SUBTITLE" ]]; then
            VF="${VF},drawtext=text='${SUBTITLE}':fontfile=/System/Library/Fonts/PingFang.ttc:fontsize=${FONT_SIZE_SUB}:fontcolor=${TEXT_COLOR}@0.7:x=(w-text_w)/2:y=${SUB_Y}:alpha='if(lt(t,${FADE_IN_DUR}),t/${FADE_IN_DUR},if(gt(t,${DURATION}-${FADE_OUT_DUR}),(${DURATION}-t)/${FADE_OUT_DUR},1))'"
        fi
        ;;
    zoom)
        # 从小放大
        VF="color=c=${BG_COLOR}:s=${WIDTH}x${HEIGHT}:d=${DURATION},format=yuv420p"
        ZOOM_SIZE="min(${FONT_SIZE_TITLE}*0.5+${FONT_SIZE_TITLE}*0.5*t/${FADE_IN_DUR}\,${FONT_SIZE_TITLE})"
        VF="${VF},drawtext=text='${TITLE}':fontfile=/System/Library/Fonts/PingFang.ttc:fontsize=${FONT_SIZE_TITLE}:fontcolor=${TEXT_COLOR}:x=(w-text_w)/2:y=${TITLE_Y}:alpha='if(lt(t,${FADE_IN_DUR}),t/${FADE_IN_DUR},if(gt(t,${DURATION}-${FADE_OUT_DUR}),(${DURATION}-t)/${FADE_OUT_DUR},1))'"
        if [[ -n "$SUBTITLE" ]]; then
            VF="${VF},drawtext=text='${SUBTITLE}':fontfile=/System/Library/Fonts/PingFang.ttc:fontsize=${FONT_SIZE_SUB}:fontcolor=${TEXT_COLOR}@0.7:x=(w-text_w)/2:y=${SUB_Y}:alpha='if(lt(t,${FADE_IN_DUR}+0.3),(t-0.3)/${FADE_IN_DUR},if(gt(t,${DURATION}-${FADE_OUT_DUR}),(${DURATION}-t)/${FADE_OUT_DUR},1))'"
        fi
        ;;
    slide)
        # 从左滑入
        VF="color=c=${BG_COLOR}:s=${WIDTH}x${HEIGHT}:d=${DURATION},format=yuv420p"
        VF="${VF},drawtext=text='${TITLE}':fontfile=/System/Library/Fonts/PingFang.ttc:fontsize=${FONT_SIZE_TITLE}:fontcolor=${TEXT_COLOR}:x='if(lt(t,${FADE_IN_DUR}),-text_w+(w/2+text_w/2)*t/${FADE_IN_DUR},(w-text_w)/2)':y=${TITLE_Y}:alpha='if(gt(t,${DURATION}-${FADE_OUT_DUR}),(${DURATION}-t)/${FADE_OUT_DUR},1)'"
        if [[ -n "$SUBTITLE" ]]; then
            VF="${VF},drawtext=text='${SUBTITLE}':fontfile=/System/Library/Fonts/PingFang.ttc:fontsize=${FONT_SIZE_SUB}:fontcolor=${TEXT_COLOR}@0.7:x='if(lt(t,${FADE_IN_DUR}+0.3),-text_w+(w/2+text_w/2)*(t-0.3)/${FADE_IN_DUR},(w-text_w)/2)':y=${SUB_Y}:alpha='if(gt(t,${DURATION}-${FADE_OUT_DUR}),(${DURATION}-t)/${FADE_OUT_DUR},1)'"
        fi
        ;;
    minimal)
        # 极简白底黑字
        VF="color=c=white:s=${WIDTH}x${HEIGHT}:d=${DURATION},format=yuv420p"
        VF="${VF},drawtext=text='${TITLE}':fontfile=/System/Library/Fonts/PingFang.ttc:fontsize=${FONT_SIZE_TITLE}:fontcolor=black:x=(w-text_w)/2:y=${TITLE_Y}:alpha='if(lt(t,0.5),t/0.5,if(gt(t,${DURATION}-0.5),(${DURATION}-t)/0.5,1))'"
        if [[ -n "$SUBTITLE" ]]; then
            VF="${VF},drawtext=text='${SUBTITLE}':fontfile=/System/Library/Fonts/PingFang.ttc:fontsize=${FONT_SIZE_SUB}:fontcolor=gray:x=(w-text_w)/2:y=${SUB_Y}:alpha='if(lt(t,0.8),t/0.8,if(gt(t,${DURATION}-0.5),(${DURATION}-t)/0.5,1))'"
        fi
        ;;
    social)
        # 社交媒体卡片（片尾）
        VF="color=c=${BG_COLOR}:s=${WIDTH}x${HEIGHT}:d=${DURATION},format=yuv420p"
        VF="${VF},drawtext=text='${TITLE}':fontfile=/System/Library/Fonts/PingFang.ttc:fontsize=${FONT_SIZE_TITLE}:fontcolor=${TEXT_COLOR}:x=(w-text_w)/2:y=(h-text_h)/2-60:alpha='if(lt(t,${FADE_IN_DUR}),t/${FADE_IN_DUR},if(gt(t,${DURATION}-${FADE_OUT_DUR}),(${DURATION}-t)/${FADE_OUT_DUR},1))'"
        
        SOCIAL_TEXT="${SOCIAL_LINKS:-关注我获取更多内容}"
        VF="${VF},drawtext=text='${SOCIAL_TEXT}':fontfile=/System/Library/Fonts/PingFang.ttc:fontsize=36:fontcolor=${TEXT_COLOR}@0.8:x=(w-text_w)/2:y=(h-text_h)/2+60:alpha='if(lt(t,${FADE_IN_DUR}+0.5),(t-0.5)/${FADE_IN_DUR},if(gt(t,${DURATION}-${FADE_OUT_DUR}),(${DURATION}-t)/${FADE_OUT_DUR},1))'"
        
        # 分割线
        VF="${VF},drawtext=text='━━━━━━━━━━━━━━━━━':fontsize=24:fontcolor=${ACCENT_COLOR}:x=(w-text_w)/2:y=(h-text_h)/2+20:alpha='if(lt(t,${FADE_IN_DUR}),t/${FADE_IN_DUR},if(gt(t,${DURATION}-${FADE_OUT_DUR}),(${DURATION}-t)/${FADE_OUT_DUR},1))'"
        ;;
    subscribe)
        # 订阅提示
        VF="color=c=${BG_COLOR}:s=${WIDTH}x${HEIGHT}:d=${DURATION},format=yuv420p"
        VF="${VF},drawtext=text='${TITLE}':fontfile=/System/Library/Fonts/PingFang.ttc:fontsize=${FONT_SIZE_TITLE}:fontcolor=${TEXT_COLOR}:x=(w-text_w)/2:y=(h-text_h)/2-80:alpha='if(lt(t,${FADE_IN_DUR}),t/${FADE_IN_DUR},if(gt(t,${DURATION}-${FADE_OUT_DUR}),(${DURATION}-t)/${FADE_OUT_DUR},1))'"
        
        # 订阅按钮样式文字
        VF="${VF},drawtext=text='👍 点赞  ⭐ 收藏  🔔 关注':fontfile=/System/Library/Fonts/Apple Color Emoji.ttc:fontsize=44:fontcolor=${ACCENT_COLOR}:x=(w-text_w)/2:y=(h-text_h)/2+40:alpha='if(lt(t,${FADE_IN_DUR}+0.5),(t-0.5)/${FADE_IN_DUR},if(gt(t,${DURATION}-${FADE_OUT_DUR}),(${DURATION}-t)/${FADE_OUT_DUR},1))'"
        
        if [[ -n "$SUBTITLE" ]]; then
            VF="${VF},drawtext=text='${SUBTITLE}':fontfile=/System/Library/Fonts/PingFang.ttc:fontsize=${FONT_SIZE_SUB}:fontcolor=${TEXT_COLOR}@0.6:x=(w-text_w)/2:y=(h-text_h)/2+120:alpha='if(lt(t,${FADE_IN_DUR}+0.8),(t-0.8)/${FADE_IN_DUR},if(gt(t,${DURATION}-${FADE_OUT_DUR}),(${DURATION}-t)/${FADE_OUT_DUR},1))'"
        fi
        ;;
    *)
        echo -e "${YELLOW}⚠️  未知模板：$TEMPLATE，使用 fade${NC}"
        TEMPLATE="fade"
        VF="color=c=${BG_COLOR}:s=${WIDTH}x${HEIGHT}:d=${DURATION},format=yuv420p"
        VF="${VF},drawtext=text='${TITLE}':fontfile=/System/Library/Fonts/PingFang.ttc:fontsize=${FONT_SIZE_TITLE}:fontcolor=${TEXT_COLOR}:x=(w-text_w)/2:y=${TITLE_Y}"
        ;;
esac

echo -e "${BLUE}🔧 生成中...${NC}"

# Logo 叠加
if [[ -n "$LOGO" && -f "$LOGO" ]]; then
    # 生成基础视频后叠加 Logo
    TEMP_BASE="/tmp/intro-base-$(date +%s).mp4"
    
    ffmpeg -y -f lavfi -i "${VF}" \
        -t "$DURATION" -c:v libx264 -crf 18 -pix_fmt yuv420p \
        "$TEMP_BASE" -loglevel warning 2>/dev/null
    
    # 叠加 Logo (居中上方)
    ffmpeg -y -i "$TEMP_BASE" -i "$LOGO" \
        -filter_complex "[1:v]scale=200:-1[logo];[0:v][logo]overlay=(W-w)/2:H/4-h/2:format=auto,fade=t=in:d=${FADE_IN_DUR},fade=t=out:st=$((DURATION-FADE_OUT_DUR)):d=${FADE_OUT_DUR}" \
        -c:v libx264 -crf 18 -pix_fmt yuv420p \
        -t "$DURATION" \
        "$OUTPUT" -loglevel warning 2>/dev/null
    
    rm -f "$TEMP_BASE"
else
    # 无 Logo，直接生成
    ffmpeg -y -f lavfi -i "${VF}" \
        -t "$DURATION" -c:v libx264 -crf 18 -pix_fmt yuv420p \
        "$OUTPUT" -loglevel warning 2>/dev/null
fi

# 添加静音音轨（避免合并视频时音频不同步）
TEMP_SILENT="/tmp/intro-silent-$(date +%s).mp4"
ffmpeg -y -i "$OUTPUT" -f lavfi -i anullsrc=r=44100:cl=stereo \
    -c:v copy -c:a aac -shortest \
    "$TEMP_SILENT" -loglevel warning 2>/dev/null && mv "$TEMP_SILENT" "$OUTPUT"

if [[ -f "$OUTPUT" ]]; then
    FILE_SIZE=$(stat -f%z "$OUTPUT" 2>/dev/null | awk '{printf "%.1f", $1/1048576}')
    echo ""
    echo -e "${GREEN}✅ ${TYPE} 生成完成！${NC}"
    echo -e "   📁 文件：$OUTPUT (${FILE_SIZE}MB)"
    echo -e "   🎨 模板：$TEMPLATE"
    echo -e "   ⏱️ 时长：${DURATION}s"
    echo ""
    echo -e "${BLUE}💡 拼接到视频：ffmpeg -f concat -safe 0 -i list.txt -c copy final.mp4${NC}"
else
    echo -e "${RED}❌ 生成失败${NC}"
    exit 1
fi
