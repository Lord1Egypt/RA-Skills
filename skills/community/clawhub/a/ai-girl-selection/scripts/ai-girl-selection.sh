#!/bin/bash
# AI Girl Selection Tool
# Daily random selection of 3 AI girl portraits

SOURCE_DIR="/Volumes/info/sex/picture/AI girls"
PREVIEW_DIR="/Users/qifengxiang/.openclaw/workspace"
AVATAR_DIR="/Users/qifengxiang/.openclaw/workspace/avatars"
PREFERENCES_FILE="/Users/qifengxiang/.openclaw/workspace/.learnings/AI-GIRL-PREFERENCES.md"

# Ensure directories exist
mkdir -p "$PREVIEW_DIR" "$AVATAR_DIR" "$(dirname $PREFERENCES_FILE)"

# Get list of image files
get_random_images() {
    cd "$SOURCE_DIR"
    ls -1 | grep -iE '\.(jpg|jpeg|png|webp)$' | sort | awk 'BEGIN{srand()} 
    {arr[NR]=$0} 
    END{
        for(i=1;i<=3;i++){
            idx=int(rand()*NR)+1; 
            print arr[idx]; 
            delete arr[idx]; 
            for(j=idx;j<NR;j++)arr[j]=arr[j+1];
            NR--
        }
    }'
}

# Select 3 random images
echo "🌹 选妃时间 - Daily AI Girl Selection"
echo "======================================"
echo "当前时间：$(date -u '+%Y-%m-%d %H:%M Asia/Shanghai')"
echo ""

RANDOM_FILES=$(get_random_images)
COUNTER=0

echo "随机选取了 3 张 AI Girl 图片：\n"
while IFS= read -r filename; do
    COUNTER=$((COUNTER+1))
    FULL_PATH="$SOURCE_DIR/$filename"
    
    # Copy to preview directory
    cp "$FULL_PATH" "$PREVIEW_DIR/preview${COUNTER}.$(echo $filename | grep -oE '\.[^.]+$')"
    
    echo "$COUNTER. $filename ✅"
done <<< "$RANDOM_FILES"

echo ""
echo "请选择一个你喜欢的："
echo '  说 "选 1" / "选 2" / "选 3"'
echo '  或 "第一个" / "第二个" / "第三个"'
echo '  或 直接说文件名'
echo ""

# Create HTML preview
cat > "$PREVIEW_DIR/selection-preview.html" << 'HTMLEOF'
<!DOCTYPE html>
<html lang="zh-CN">
<head>
    <meta charset="UTF-8">
    <meta name="viewport" content="width=device-width, initial-scale=1.0">
    <title>🌹 选妃时间</title>
    <style>
        body { 
            font-family: -apple-system, BlinkMacSystemFont, sans-serif;
            background: linear-gradient(135deg, #667eea 0%, #764ba2 100%); 
            min-height: 100vh;
            padding: 40px;
            margin: 0;
        }
        .container { 
            max-width: 1400px; 
            margin: 0 auto;
            background: rgba(255,255,255,0.95);
            border-radius: 20px;
            padding: 40px;
            box-shadow: 0 20px 60px rgba(0,0,0,0.3);
        }
        h1 { color: #667eea; text-align: center; font-size: 2.8em; margin-bottom: 10px; }
        h2 { color: #333; text-align: center; font-size: 1.2em; margin-bottom: 40px; font-weight: normal; }
        .gallery { display: grid; grid-template-columns: repeat(auto-fit, minmax(350px, 1fr)); gap: 40px; margin-top: 40px; }
        .card { 
            background: white; 
            border-radius: 16px; 
            padding: 25px; 
            box-shadow: 0 8px 24px rgba(0,0,0,0.12); 
            text-align: center;
            transition: all 0.3s ease;
            border: 2px solid transparent;
        }
        .card:hover { 
            transform: translateY(-8px);
            box-shadow: 0 16px 40px rgba(0,0,0,0.2);
            border-color: #667eea;
        }
        .card img { 
            max-width: 100%; 
            max-height: 500px;
            border-radius: 12px;
            box-shadow: 0 4px 12px rgba(0,0,0,0.1);
            object-fit: contain;
        }
        .card-title { font-size: 1.6em; font-weight: bold; color: #333; margin-bottom: 15px; }
        .card-desc { color: #666; margin-top: 10px; font-size: 0.9em; }
        .instruction { text-align: center; padding: 30px; margin-top: 40px; background: #f8f9fa; border-radius: 12px; }
        .instruction strong { color: #667eea; font-size: 1.3em; }
    </style>
</head>
<body>
    <div class="container">
        <h1>🌹 选妃时间</h1>
        <h2>Daily AI Girl Portrait Selection - $(date -u '+%Y-%m-%d %H:%M Asia/Shanghai')</h2>
        <div class="gallery">
HTMLEOF

# Add cards for each preview
for i in 1 2 3; do
    PREVIEW_FILE="$PREVIEW_DIR/preview${i}.*"
    PREVIEW_FILE=$(ls $PREVIEW_FILE 2>/dev/null | head -1)
    if [ -f "$PREVIEW_FILE" ]; then
        cat >> "$PREVIEW_DIR/selection-preview.html" << EOF
            <div class="card">
                <div class="card-title">👉 候选 $i 👈</div>
                <img src="$PREVIEW_FILE" alt="候选者 $i">
                <div class="card-desc">Filename: $(basename "$PREVIEW_FILE")</div>
            </div>
EOF
    fi
done

cat >> "$PREVIEW_DIR/selection-preview.html" << 'HTMLEOF'
        </div>
        <div class="instruction">
            <strong>请告诉我你的选择！</strong><br>
            说 <strong>"选 1"</strong> / <strong>"选 2"</strong> / <strong>"选 3"</strong><br>
            或 <strong>"第一个"</strong> / <strong>"第二个"</strong> / <strong>"第三个"</strong><br>
            或 <strong>直接说文件名</strong>
        </div>
    </div>
</body>
</html>
HTMLEOF

# Open in browser
open "$PREVIEW_DIR/selection-preview.html"

echo "✅ HTML preview created: $PREVIEW_DIR/selection-preview.html"
echo "   (Opened in your default browser)"
echo ""
echo "现在请在聊天中告诉我你的选择！"
