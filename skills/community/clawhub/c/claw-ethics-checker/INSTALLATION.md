# 🦀 Claw-Ethics-Checker 安装指南

## 简介
Claw-Ethics-Checker 是一个为AI助手设计的伦理合规检查工具，帮助自动识别风险任务，确保合法合规操作。

## 系统要求
- Python 3.8+
- OpenClaw 1.0+
- 至少10MB磁盘空间

## 安装方法

### 方法1：通过ClawdHub安装（推荐）
```bash
# 安装clawdhub CLI（如果尚未安装）
npm install -g clawdhub

# 搜索skill
clawdhub search ethics-checker

# 安装skill
clawdhub install claw-ethics-checker
```

### 方法2：手动安装
```bash
# 1. 下载skill文件
git clone https://github.com/openclaw/claw-ethics-checker.git
# 或直接下载
wget https://github.com/openclaw/claw-ethics-checker/archive/main.zip

# 2. 复制到OpenClaw技能目录
mkdir -p ~/.openclaw/skills/
cp -r claw-ethics-checker ~/.openclaw/skills/

# 3. 配置OpenClaw
# 编辑 ~/.openclaw/config.yaml，添加：
skills:
  claw-ethics-checker:
    enabled: true
    risk_threshold: medium
    require_human_review: true
```

### 方法3：Python包安装
```bash
# 安装为Python包
pip install claw-ethics-checker

# 在Python中使用
from claw_ethics_checker import EthicsChecker
checker = EthicsChecker()
```

## 快速开始

### 基本使用
```python
from claw_ethics_checker import EthicsChecker

# 创建检查器
checker = EthicsChecker()

# 分析任务
task = {
    'description': '监控竞争对手网站价格',
    'client': '电商公司',
    'methods': ['web_scraping'],
    'data_source': '公开网站'
}

result = checker.analyze_task('竞争分析', task)

# 查看结果
print(f'风险等级: {result.risk_level}')
print(f'是否合规: {result.is_compliant}')
print(f'建议: {result.recommendations}')
```

### 集成到OpenClaw工作流
```python
# 在OpenClaw技能中使用
def handle_task(task_request):
    # 先进行伦理检查
    ethics_result = ethics_checker.analyze_task(
        task_request.description,
        task_request.details
    )
    
    if ethics_result.risk_level == 'high':
        return {
            'status': 'rejected',
            'reason': '高风险任务，需要人工审核',
            'ethics_check': ethics_result.to_dict()
        }
    
    # 如果合规，继续处理任务
    return process_task(task_request)
```

## 配置选项

### 配置文件示例
```yaml
# config.yaml
claw_ethics_checker:
  # 基本配置
  enabled: true
  risk_threshold: medium  # low/medium/high
  
  # 审核设置
  require_human_review: true
  human_review_threshold: medium
  
  # 日志设置
  log_decisions: true
  log_file: /var/log/claw_ethics.log
  
  # 规则设置
  custom_rules:
    - name: '公司特定规则'
      condition: 'client == "内部使用"'
      action: 'auto_approve'
    
    - name: '高风险客户'
      condition: 'client in ["高风险列表"]'
      action: 'always_review'
  
  # 通知设置
  notifications:
    email: 'admin@example.com'
    slack_webhook: 'https://hooks.slack.com/...'
```

### 环境变量
```bash
# 可以通过环境变量覆盖配置
export CLAW_ETHICS_RISK_THRESHOLD=high
export CLAW_ETHICS_LOG_FILE=/tmp/ethics.log
export CLAW_ETHICS_REQUIRE_HUMAN_REVIEW=false
```

## 测试安装

### 运行测试套件
```bash
cd ~/.openclaw/skills/claw-ethics-checker
python3 test_ethics_checker.py
```

### 验证安装
```python
# 验证脚本
import sys
try:
    from claw_ethics_checker import EthicsChecker
    checker = EthicsChecker()
    print('✅ Claw-Ethics-Checker 安装成功！')
    print(f'版本: {checker.__version__}')
except ImportError as e:
    print('❌ 安装失败:', e)
    sys.exit(1)
```

## 故障排除

### 常见问题

**Q: 导入错误 "No module named 'claw_ethics_checker'"**
```bash
# 确保在Python路径中
export PYTHONPATH=$PYTHONPATH:/path/to/claw-ethics-checker
# 或使用绝对导入
import sys
sys.path.append('/path/to/claw-ethics-checker')
```

**Q: OpenClaw找不到skill**
```bash
# 检查技能目录
ls ~/.openclaw/skills/
# 确保目录结构正确
# 应该是: ~/.openclaw/skills/claw-ethics-checker/SKILL.md
```

**Q: 配置不生效**
```yaml
# 检查配置文件语法
# 确保使用正确的缩进（2个空格）
skills:
  claw-ethics-checker:
    enabled: true  # 注意缩进
```

### 获取帮助
- GitHub Issues: https://github.com/openclaw/claw-ethics-checker/issues
- 文档: https://docs.openclaw.ai/skills/ethics-checker
- 社区: Moltbook @TestClaw_001
- 邮箱: support@openclaw.ai

## 更新

### 检查更新
```bash
# 通过ClawdHub
clawdhub update claw-ethics-checker

# 手动更新
cd ~/.openclaw/skills/claw-ethics-checker
git pull origin main
```

### 版本历史
- v0.1.0 (2026-02-09): 初始发布
  - 基础伦理检查功能
  - 风险等级评估
  - 测试套件

## 下一步
安装完成后，建议：
1. 阅读 [USAGE.md](USAGE.md) 了解详细使用方法
2. 查看 [EXAMPLES.md](EXAMPLES.md) 学习实际案例
3. 配置适合你工作流的规则
4. 集成到现有系统中

---
*如有问题，请查阅文档或联系支持* 🦀