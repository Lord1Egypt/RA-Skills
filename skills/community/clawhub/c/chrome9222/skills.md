{
  "name": "Chrome9222端口启动",
  "id": "chrome_9222_launch",
  "version": "1.0.0",
  "description": "一键通过9222调试端口启动Chrome",
  "config": {
    "browser": {
      "enabled": true,
      "type": "chrome",
      "remoteDebuggingPort": 9222,
      "headless": false
    }
  },
  "actions": [
    {
      "name": "启动Chrome(9222端口)",
      "id": "launch_chrome_9222",
      "parameters": [],
      "exec": {
        "type": "script",
        "lang": "javascript",
        "code": "async function execute() { try { // 杀死残留Chrome进程 const { execSync } = require('child_process'); execSync('taskkill /f /im chrome.exe 2>nul'); // 启动Chrome（9222端口） execSync('\"C:\\Program Files\\Google\\Chrome\\Application\\chrome.exe\" --remote-debugging-port=9222 --user-data-dir=C:\\temp\\chrome_test'); return '✅ Chrome已通过9222端口启动！'; } catch (error) { return `❌ 启动失败：${error.message}`; } }"
      }
    }
  ],
  "triggers": []
}