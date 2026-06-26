#!/bin/bash
# qmd-rebuild-serial.sh - 串行重建 per agent qmd index
#
# 为什么串行:
#   32 个并发 reindex 抢 batch embed lock + GPU = timeout 砍
#   串行 30-50s/agent, 32 个 16-20 min 跑完
#   串行 GPU 持续 7GB 利用率, 并发反而 timeout 全部失败
#
# 用法: bash qmd-rebuild-serial.sh

set +e  # 不要让单个失败中断整个 batch

LOG=/tmp/qmd-serial-reindex.log
DONE_DIR=/tmp/qmd-done
mkdir -p "$DONE_DIR"

# ⚠️ 修改这里: 改成你的 agent 列表
# 33 个 agent: main + 32 个其他
# 如果你的 agent 数量不同, 改这个数组
AGENTS=(
    agent-main agent-a agent-b agent-c agent-d agent-e
    agent-f agent-g agent-h agent-i agent-j agent-k
    agent-l agent-m agent-n agent-o agent-p agent-q
    agent-r agent-s agent-t agent-u agent-v agent-w
    agent-x agent-y agent-z
    reader-1 reader-2 reader-3 reader-4 reader-5
)

echo "[$(date +%H:%M:%S)] 串行 reindex 启动: ${#AGENTS[@]} 个 agent" > $LOG
echo "[$(date +%H:%M:%S)] 注意: 串行 30-50s/agent, 不并发" >> $LOG

# 找需要跑 (vectors=0) 的 agent
to_run=()
for a in "${AGENTS[@]}"; do
    db="\$HOME/.openclaw/agents/$a/qmd/xdg-cache/qmd/index.sqlite"
    if [ -f "$db" ]; then
        vectors=$(sqlite3 "$db" "SELECT COUNT(*) FROM content_vectors;" 2>/dev/null)
        if [ "$vectors" -lt "1" ] 2>/dev/null; then
            # 跳过已 done 的
            if [ ! -f "$DONE_DIR/$a" ]; then
                to_run+=("$a")
            fi
        fi
    fi
done

echo "[$(date +%H:%M:%S)] 待跑: ${#to_run[@]} 个 agent" >> $LOG
for a in "${to_run[@]}"; do
    echo "  - $a" >> $LOG
done
echo "" >> $LOG

if [ ${#to_run[@]} -eq 0 ]; then
    echo "[$(date +%H:%M:%S)] 没有需要跑的 agent (全部都有 vectors)" >> $LOG
    cat $LOG
    exit 0
fi

success=0
fail=0
failed_agents=()

for a in "${to_run[@]}"; do
    echo "[$(date +%H:%M:%S)] 开始: $a" >> $LOG
    start=$(date +%s)

    if openclaw memory index --force --agent "$a" --verbose >> $LOG 2>&1; then
        end=$(date +%s)
        dur=$((end - start))
        db="\$HOME/.openclaw/agents/$a/qmd/xdg-cache/qmd/index.sqlite"
        vectors=$(sqlite3 "$db" "SELECT COUNT(*) FROM content_vectors;" 2>/dev/null)
        size=$(stat -c %s "$db" 2>/dev/null)
        echo "[$(date +%H:%M:%S)] ✓ $a 完成 (${dur}s, ${vectors} vectors, ${size}B)" >> $LOG
        touch "$DONE_DIR/$a"
        success=$((success + 1))
    else
        end=$(date +%s)
        dur=$((end - start))
        echo "[$(date +%H:%M:%S)] ✗ $a 失败 (${dur}s)" >> $LOG
        fail=$((fail + 1))
        failed_agents+=("$a")
    fi
done

echo "" >> $LOG
echo "[$(date +%H:%M:%S)] 串行 reindex 完成: $success 成功, $fail 失败" >> $LOG
if [ $fail -gt 0 ]; then
    echo "失败的 agent:" >> $LOG
    for a in "${failed_agents[@]}"; do
        echo "  - $a" >> $LOG
    done
fi

cat $LOG
