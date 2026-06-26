#!/bin/bash

# Aria2 Download - Add downloads and query status via Aria2 RPC
# Usage: 
#   aria2-download add "URL" [filename]     - 添加下载
#   aria2-download status <gid>             - 查询下载状态
#   aria2-download progress <gid>           - 实时监控下载进度
#   aria2-download watch <gid> [interval]    - 实时监控下载进度 (每秒更新)
#   aria2-download list                     - 列出活跃任务

RPC_URL="${ARIA2_RPC_URL:-http://localhost:6800/jsonrpc}"
SECRET="${ARIA2_SECRET:-}"
DIR="${ARIA2_DIR:-}"

CMD="$1"
shift

add_download() {
  URL="$1"
  FILENAME="$2"
  
  OPTIONS_JSON="{\"max-connection-per-server\":16,\"split\":16,\"min-split-size\":\"1M\""
  [ -n "$DIR" ] && OPTIONS_JSON="${OPTIONS_JSON},\"dir\":\"$DIR\""
  [ -n "$FILENAME" ] && OPTIONS_JSON="${OPTIONS_JSON},\"out\":\"$FILENAME\""
  OPTIONS_JSON="${OPTIONS_JSON}}"
  
  if [ -n "$SECRET" ]; then
    RPC_PAYLOAD="{\"jsonrpc\":\"2.0\",\"method\":\"aria2.addUri\",\"id\":1,\"params\":[\"token:${SECRET}\",[\"$URL\"],$OPTIONS_JSON]}"
  else
    RPC_PAYLOAD="{\"jsonrpc\":\"2.0\",\"method\":\"aria2.addUri\",\"id\":1,\"params\":[[\"URL\"],$OPTIONS_JSON]}"
  fi
  
  RESPONSE=$(curl -s -X POST "$RPC_URL" -H "Content-Type: application/json" -d "$RPC_PAYLOAD")
  
  if echo "$RESPONSE" | grep -q '"error"'; then
    ERROR_MSG=$(echo "$RESPONSE" | grep -oP '"message":\s*"\K[^"]+' | head -1)
    echo "{\"success\": false, \"error\": \"${ERROR_MSG:-RPC Error}\"}"
    exit 1
  fi
  
  GID=$(echo "$RESPONSE" | grep -oP '"result":\s*"\K[^"]+' | head -1)
  if [ -n "$GID" ]; then
    echo "{\"success\": true, \"gid\": \"${GID}\", \"url\": \"${URL}\"}"
  else
    echo "{\"success\": false, \"error\": \"添加失败\"}"
    exit 1
  fi
}

get_status() {
  GID="$1"
  
  if [ -n "$SECRET" ]; then
    RPC_PAYLOAD="{\"jsonrpc\":\"2.0\",\"method\":\"aria2.tellStatus\",\"id\":1,\"params\":[\"token:${SECRET}\",\"$GID\"]}"
  else
    RPC_PAYLOAD="{\"jsonrpc\":\"2.0\",\"method\":\"aria2.tellStatus\",\"id\":1,\"params\":[\"$GID\"]}"
  fi
  
  RESPONSE=$(curl -s -X POST "$RPC_URL" -H "Content-Type: application/json" -d "$RPC_PAYLOAD")
  
  if echo "$RESPONSE" | grep -q '"error"'; then
    echo "{\"success\": false, \"error\": \"查询失败\"}"
    exit 1
  fi
  
  echo "$RESPONSE"
}

get_progress() {
  GID="$1"
  
  if [ -n "$SECRET" ]; then
    RPC_PAYLOAD="{\"jsonrpc\":\"2.0\",\"method\":\"aria2.tellStatus\",\"id\":1,\"params\":[\"token:${SECRET}\",\"$GID\",[\"status\",\"totalLength\",\"completedLength\",\"downloadSpeed\",\"files\"]]}"
  else
    RPC_PAYLOAD="{\"jsonrpc\":\"2.0\",\"method\":\"aria2.tellStatus\",\"id\":1,\"params\":[\"$GID\",[\"status\",\"totalLength\",\"completedLength\",\"downloadSpeed\",\"files\"]]}"
  fi
  
  RESPONSE=$(curl -s -X POST "$RPC_URL" -H "Content-Type: application/json" -d "$RPC_PAYLOAD")
  
  if echo "$RESPONSE" | grep -q '"error"'; then
    echo "{\"success\": false, \"error\": \"任务不存在或已完成\"}"
    exit 1
  fi
  
  node -e "
    const r = JSON.parse('$RESPONSE');
    if (!r.result) { console.log('{\"success\": false, \"error\": \"无结果\"}'); process.exit(0); }
    
    const s = r.result;
    const total = parseInt(s.totalLength) || 0;
    const completed = parseInt(s.completedLength) || 0;
    const speed = parseInt(s.downloadSpeed) || 0;
    const percent = total > 0 ? ((completed / total) * 100).toFixed(1) : 0;
    
    const filename = s.files && s.files[0] ? s.files[0].path : 'unknown';
    const name = filename.split('/').pop();
    
    console.log(JSON.stringify({
      success: true,
      gid: '$GID',
      status: s.status,
      name: name,
      total: total,
      completed: completed,
      speed: speed,
      speedHuman: speed > 1024*1024 ? (speed/1024/1024).toFixed(1)+'MB/s' : (speed/1024).toFixed(1)+'KB/s',
      percent: percent + '%',
      eta: speed > 0 ? Math.round((total - completed) / speed) + 's' : null
    }));
  "
}

wait_complete() {
  GID="$1"
  INTERVAL="${2:-2}"
  
  while true; do
    if [ -n "$SECRET" ]; then
      RPC_PAYLOAD="{\"jsonrpc\":\"2.0\",\"method\":\"aria2.tellStatus\",\"id\":1,\"params\":[\"token:${SECRET}\",\"$GID\",[\"status\",\"totalLength\",\"completedLength\",\"downloadSpeed\",\"files\",\"fileSize\",\"dir\"]]}"
    else
      RPC_PAYLOAD="{\"jsonrpc\":\"2.0\",\"method\":\"aria2.tellStatus\",\"id\":1,\"params\":[\"$GID\",[\"status\",\"totalLength\",\"completedLength\",\"downloadSpeed\",\"files\",\"fileSize\",\"dir\"]]}"
    fi
    
    RESPONSE=$(curl -s -X POST "$RPC_URL" -H "Content-Type: application/json" -d "$RPC_PAYLOAD" 2>/dev/null)
    
    if echo "$RESPONSE" | grep -q '"error"'; then
      echo ""
      echo "❌ 任务已完成或不存在"
      break
    fi
    
    node -e "
      const r = JSON.parse('$RESPONSE');
      const s = r.result || {};
      const status = s.status;
      const total = parseInt(s.totalLength) || 0;
      const completed = parseInt(s.completedLength) || 0;
      const speed = parseInt(s.downloadSpeed) || 0;
      const percent = total > 0 ? ((completed / total) * 100).toFixed(1) : 0;
      const filename = s.files && s.files[0] ? s.files[0].path.split('/').pop() : 'unknown';
      const dir = s.dir || '$DIR';
      const totalSize = (total / 1024 / 1024).toFixed(2);
      const completedSize = (completed / 1024 / 1024).toFixed(2);
      
      if (status === 'complete') {
        console.log('');
        console.log('━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━');
        console.log('✅ 下载完成！');
        console.log('━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━');
        console.log('📁 文件: ' + filename);
        console.log('📂 路径: ' + dir);
        console.log('💾 大小: ' + totalSize + ' MB (1文件)');
        console.log('📊 状态: 已完成');
        console.log('📈 进度: 100%');
        console.log('📥 下载量: ' + completedSize + ' MB');
        console.log('━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━');
        process.exit(0);
      }
      
      const bar = '█'.repeat(Math.floor(percent/5)) + '░'.repeat(20-Math.floor(percent/5));
      const speedStr = speed > 1024*1024 ? (speed/1024/1024).toFixed(1)+'MB/s' : (speed/1024).toFixed(1)+'KB/s';
      const eta = speed > 0 ? Math.round((total - completed) / speed) + '秒' : '';
      
      process.stdout.write('\\r[' + bar + '] ' + percent + '% | ' + speedStr + ' | ' + filename + (eta ? ' | 剩余: '+eta : ''));
    "
    
    RESULT=$?
    if [ $RESULT -eq 0 ]; then
      break
    fi
    
    sleep "$INTERVAL"
  done
}

case "$CMD" in
  add|"")
    if [ -z "$1" ]; then
      echo "Usage: aria2-download add \"<URL>\" [filename]"
      exit 1
    fi
    add_download "$@"
    ;;
    
  status)
    if [ -z "$1" ]; then
      echo "Usage: aria2-status <gid>"
      exit 1
    fi
    get_status "$1"
    ;;
    
  progress)
    if [ -z "$1" ]; then
      echo "Usage: aria2-progress <gid>"
      exit 1
    fi
    get_progress "$1"
    ;;
    
  watch)
    if [ -z "$1" ]; then
      echo "Usage: aria2-watch <gid> [interval]"
      exit 1
    fi
    wait_complete "$1" "$2"
    ;;
    
  wait)
    if [ -z "$1" ]; then
      echo "Usage: aria2-wait <gid> [interval]"
      exit 1
    fi
    wait_complete "$1" "$2"
    ;;
    
  list)
    if [ -n "$SECRET" ]; then
      RPC_PAYLOAD="{\"jsonrpc\":\"2.0\",\"method\":\"aria2.tellActive\",\"id\":1,\"params\":[\"token:${SECRET}\"]}"
    else
      RPC_PAYLOAD="{\"jsonrpc\":\"2.0\",\"method\":\"aria2.tellActive\",\"id\":1,\"params\":[]}"
    fi
    
    RESPONSE=$(curl -s -X POST "$RPC_URL" -H "Content-Type: application/json" -d "$RPC_PAYLOAD")
    echo "$RESPONSE"
    ;;
    
  *)
    echo "Usage:"
    echo "  aria2-download add \"<URL>\" [filename]  - 添加下载"
    echo "  aria2-download status <gid>             - 查询状态 (JSON)"
    echo "  aria2-download progress <gid>           - 单次进度 (JSON)"
    echo "  aria2-download watch <gid> [interval]  - 实时监控 & 完成后输出详情"
    echo "  aria2-download wait <gid>              - 等待下载完成"
    echo "  aria2-download list                    - 列出活跃任务"
    ;;
esac
