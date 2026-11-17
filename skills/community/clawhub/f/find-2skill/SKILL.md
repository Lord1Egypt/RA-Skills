name: example-skill
description: 这是一个示例技能，用于演示 ClawHub 技能规范。
version: 1.0.0
emoji: 🛠️
homepage: https://github.com/yourusername/example-skill
metadata:
  openclaw:
    requires:
      env:
        - API_KEY
        - BASE_URL
      bins:
        - curl
        - jq
      anyBins:
        - python3
        - python
    primaryEnv: API_KEY
    envVars:
      - name: API_KEY
        required: true
        description: 用于认证的 API 密钥
      - name: BASE_URL
        required: false
        description: 自定义 API 基础 URL，默认为 https://api.example.com
      - name: TIMEOUT
        required: false
        description: 请求超时时间（秒），默认 30
    os:
      - linux
      - macos
    always: false
    install:
      - description: "安装 Python 依赖"
        command: "pip install -r requirements.txt"
      - description: "安装系统依赖（Ubuntu/Debian）"
        command: "sudo apt-get install -y curl jq"
        os: linux
      - description: "安装系统依赖（macOS）"
        command: "brew install curl jq"
        os: macos
config:
  skill:
    example:
      retryCount: 3
      logLevel: info