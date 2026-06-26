---
name: aviation-healthcheck
description: 航空维修健康检查 - FAA/EASA/CAAC适航指令、航空安全通告、MRO行业新闻、波音空客技术通告、OpenClaw状态、磁盘空间
---

# 航空维修健康检查系统

## 概述

贾维斯的航空维修资讯与系统健康双重检查。

## 检查项目

### 1. 航空维修资讯 (每日)

#### FAA Airworthiness Directives (AD)
- **来源**: https://ad.faa.gov
- **关注**: 发动机、电子系统、结构相关AD
- **频率**: 每日检查

#### EASA Airworthiness Directives
- **来源**: https://ad.easa.europa.eu
- **关注**: 紧急AD、发动机相关指令
- **频率**: 每日检查

#### CAAC适航指令
- **来源**: https://www.caac.gov.cn (适航审定司)
- **关注**: 国内航空公司受影响的相关指令
- **频率**: 每日检查

#### 航空安全通告
- FAA Safety Alerts: https://www.faa.gov/news/safety_alerts
- EASA Safety Information: https://www.easa.europa.eu/safety-info

#### MRO行业新闻
- Avionics International: https://www.aviationtoday.com/category/mro/
- Leeham News: https://leehamnews.com
- Simple Flying: https://simpleflying.com
- Air Cargo News: https://aircargonews.com
- Aviation Herald: https://avherald.com

#### 波音/空客服务通告
- Boeing ADS: https://myboeingfleet.com
- Airbus Airworthiness: https://myairbusfleet.com

### 2. 系统健康检查

#### OpenClaw 状态
```bash
openclaw status
openclaw health --json
```

#### 磁盘空间
```bash
df -h
```

#### 安全审计
```bash
openclaw security audit
openclaw update status
```

## 执行流程

1. **航空资讯收集**: 搜索并汇总最新适航指令和行业新闻
2. **系统状态检查**: OpenClaw 运行状态、磁盘空间
3. **生成报告**: 输出格式化检查报告

## 输出格式

```
═══════════════════════════════════════
        ✈️ 航空维修健康检查报告
═══════════════════════════════════════

📅 检查时间: YYYY-MM-DD HH:mm

【航空资讯更新】
✓ FAA AD: X 条新指令
✓ EASA AD: X 条新指令  
✓ CAAC: X 条新指令
✓ 行业新闻: X 条更新
✓ 重要事件: X 条

【系统状态】
✓ OpenClaw: 运行中/异常
✓ 磁盘空间: XX% 可用
✓ 安全审计: 通过/需关注

【建议事项】
• ...

═══════════════════════════════════════
```

## Cron 调度建议

建议每日定时执行 (通过 openclaw cron add):

- `aviation-healthcheck:daily` - 每日航空资讯 + 系统检查
- 时间: 09:00, 15:00, 21:00 (参考 HEARTBEAT.md)

## 资讯关键词

搜索时关注:
- Engine (发动机): CFM56, LEAP, PW1100G, Trent 1000
- Avionics (航空电子): EFIS, FMS, TCAS, ADS-B
- Structure (结构): Fuselage, Wing, Landing Gear
- Airworthiness (适航): AD, Emergency AD, SFAR
