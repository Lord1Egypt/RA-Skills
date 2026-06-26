# 飞书应用配置指南

## 步骤1：创建飞书自建应用
1. 打开飞书开放平台：https://open.feishu.cn/
2. 登录企业管理员账号，创建「企业自建应用」
3. 应用名称随便填写，比如「文档导出工具」

## 步骤2：开通权限
在应用的「权限管理」页面，开通以下权限：
- 「查看文档」权限：`docx:readonly`
- 「查看云空间文件」权限：`drive:readonly`

权限申请后需要企业管理员审批，审批通过后才能使用。

## 步骤3：配置环境变量
获取应用的`APP ID`和`APP SECRET`，在系统环境变量中添加：
```bash
# Windows
set FEISHU_APP_ID=your_app_id
set FEISHU_APP_SECRET=your_app_secret

# macOS/Linux
export FEISHU_APP_ID=your_app_id
export FEISHU_APP_SECRET=your_app_secret
```

## 步骤4：发布应用
在飞书开放平台发布应用，选择「企业内部发布」，发布后即可使用。
