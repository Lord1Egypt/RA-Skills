#!/bin/bash
NAS_HOST="user@192.168.1.100"
QBT_SOCK="/home/user/qbt.sock"
QBT_PASSWORD="your_password"

# Check SSH connection
if ! ssh -o BatchMode=yes -o ConnectTimeout=5 $NAS_HOST exit 2>/dev/null; then
  echo "Error: Cannot connect to NAS. Please configure SSH key authentication:"
  echo "  ssh-copy-id $NAS_HOST"
  exit 1
fi

case "$1" in
  list)
    if [[ "$2" == "-all" ]]; then
      ssh $NAS_HOST "curl -s --unix-socket $QBT_SOCK -X POST http://localhost/api/v2/auth/login -d 'username=admin&password=$QBT_PASSWORD' -c /tmp/qbt_cookie >/dev/null && curl -s --unix-socket $QBT_SOCK -b /tmp/qbt_cookie http://localhost/api/v2/torrents/info" | python3 -c "import sys,json; data=json.load(sys.stdin); [print(f\"{t['name'][:60]:60} {t['state']:12} {t['progress']*100:5.1f}% {t['dlspeed']/1024/1024:6.1f}MB/s\") for t in data]"
    else
      ssh $NAS_HOST "curl -s --unix-socket $QBT_SOCK -X POST http://localhost/api/v2/auth/login -d 'username=admin&password=$QBT_PASSWORD' -c /tmp/qbt_cookie >/dev/null && curl -s --unix-socket $QBT_SOCK -b /tmp/qbt_cookie http://localhost/api/v2/torrents/info" | python3 -c "import sys,json; data=json.load(sys.stdin); [print(f\"{t['name'][:60]:60} {t['state']:12} {t['progress']*100:5.1f}% {t['dlspeed']/1024/1024:6.1f}MB/s\") for t in data if t['progress'] < 1.0]"
    fi
    ;;
  add)
    if [[ "$2" =~ ^magnet: ]]; then
      ssh $NAS_HOST "curl -s --unix-socket $QBT_SOCK -X POST http://localhost/api/v2/auth/login -d 'username=admin&password=$QBT_PASSWORD' -c /tmp/qbt_cookie && curl -s --unix-socket $QBT_SOCK -b /tmp/qbt_cookie -X POST http://localhost/api/v2/torrents/add -d 'urls=$2'"
      echo "Magnet link added"
    elif [[ -f "$2" ]]; then
      scp "$2" $NAS_HOST:/tmp/torrent.tmp
      ssh $NAS_HOST "curl -s --unix-socket $QBT_SOCK -X POST http://localhost/api/v2/auth/login -d 'username=admin&password=$QBT_PASSWORD' -c /tmp/qbt_cookie && curl -s --unix-socket $QBT_SOCK -b /tmp/qbt_cookie -X POST http://localhost/api/v2/torrents/add -F 'torrents=@/tmp/torrent.tmp'"
      echo "Torrent file added"
    else
      echo "Error: Invalid URL or file not found"
      exit 1
    fi
    ;;
  *)
    echo "Usage: $0 {list|add <url|file>}"
    exit 1
    ;;
esac
