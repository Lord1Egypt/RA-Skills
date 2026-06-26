# SKILL.md

**License:** MIT  
**Copyright:** 2026 perrykono-debug

---

---
name: enterprise-service-starter
description: 企服助手一键初始化技能。当新用户输入"@企服助手初始化"、"@企服助手 install"、"安装企服助手"、"enterprise-service install"时触发。自动检测并安装8个核心依赖技能（contract-renewal、fee-collection、enterprise-customer-management、inventory-monitor、service-matching、workorder-dispatch、visit-management、enterprise-service-assistant），然后引导用户配置项目知识库。
---

# 企服助手 - 一键初始化技能

## 🚀 触发方式

当新用户输入以下**任一关键词**时，此技能自动触发：

- `@企服助手初始化`
- `@企服助手 install`
- `/install enterprise-service`
- `安装企服助手`
- `enterprise-service install`

---

## 📋 自动化安装流程

### 第一步：检测并安装依赖技能

使用 `skillhub_install` 工具依次安装以下8个核心技能：

1. contract-renewal - 合同续租预警
2. fee-collection - 费用催缴管理
3. enterprise-customer-management - 客户管理中心
4. inventory-monitor - 库存监控与补货提醒
5. service-matching - C+服务需求匹配
6. workorder-dispatch - 工单分派与SLA监控
7. visit-management -走访计划管理与提醒
8. enterprise-service-assistant -企业服务智能助手主技能

**执行方式**：
```
对每个技能调用：skillhub_install(action="install_skill", skillName="<skill-name>")
```

###第二步：验证安装echo""===验证安袭===""foreach skill in "${SKILLS[@]}"; do


      if!openclaw sk lls list|grep-q "$skill"; then


        echo ""❌$sk ill installation failed!"""
        exit1fi



    done
 
ech o ""✅ All dependencies installed successfully!""

---

## 📝第三步：引导配置项目知识库（重要！）

安装完成后，**必须引导用户创建自己的项目知识库**。

⚠️ **重要提示**：每个用户的项目配置是独立的，包含：
- Excel数据源路径（如 `/Users/yourname/示例产业园AC+服务.xlsx`）
-  企业微信 Webhook URL
  
### 📋下一步操作指南（告诉用户）：```markdown🎉企服助手核心技有安袭完成！

###📂创建你的项目知识库：

1.**找到你的workspace目录**（通常是 `~/.openclaw /workspace/`或自定义路径）

2.**创建knowledge目录**（如果不存在）：
   bashmkdir-p knowledge
  
3.**创建 PROJECT_KB.md**：参考以下模板创建你自己的配置文件中txt#项目名称项目名称：-数据类型：`你的Excel文件路径`-企业微信Webhook：`你的Webhook地址`-业务规则：根据自身需求调整
    
4.**重启OpenCla **，让配置生效！

---

##💡注意事项



不要复制他人的PROJECT_KB.md直接使只作参考模板！
每个用户的Excel文件路径不同，必须修改！
企业微信Webhook是敏感信息，不要泄露！

是否需要我帮你生成一个性的PROJECT_KB.md模板？
```
