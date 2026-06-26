---
name: carkey
description: 查询车辆位置和车况信息（车锁、车门、车窗、空调等状态）/ Query vehicle location and condition information.
---

## 概述 / Overview

适用于已经加装 Tika 数字钥匙产品并完成 App 绑定的车辆。  
Use this skill only after the vehicle has installed the Tika Digital Key product and completed App binding.

官网 / Official website: `https://www.tikakey.com/`

API Key 获取路径：乘趣 App -> 帮助中心 -> 热门功能 -> Skill。  
API Key path: Chengqu App -> Help Center -> Popular Features -> Skill.

## 触发场景 / Triggers

- 用户查询车辆位置或询问“车在哪儿” / User asks where the car is
- 用户请求查询车况信息 / User asks for vehicle condition
- 用户询问车辆状态，例如车锁、车门、车窗、空调是否开启 / User asks about locks, doors, windows, or A/C
- 用户需要获取车辆详细信息，例如 SN、VIN、档位、电源状态 / User asks for SN, VIN, gear, or power status
- 缺少认证信息时，引导用户提供完整 API Key，并优先建议使用环境变量 / If auth is missing, ask for the full API Key and recommend environment variables first

## 核心配置 / Core Config

| 配置项 | 值 |
|--------|-----|
| API 地址 | `https://openapi.nokeeu.com/iot/v1/condition` |
| 缓存文件 | `~/.skill_carkey_cache.json` |
| 认证格式 | App 生成的完整 `API Key` |

## 认证流程 / Auth Flow

1. 首次使用时，引导用户先在 App 中获取完整 API Key / For first-time use, ask the user to obtain the full API Key from the App
2. 优先建议用户配置环境变量 `TIKA_API_KEY` / Recommend `TIKA_API_KEY` as the primary setup method
3. 如用户希望后续免配置使用，再写入 `~/.skill_carkey_cache.json` / If the user wants repeated local use, then save it to `~/.skill_carkey_cache.json`
4. 后续查询优先读取环境变量，其次读取本地缓存 / Query flow should prefer environment variables, then local cache
5. 需要时可只检查认证状态，不发起网络请求 / Support auth check without network request
6. 支持通过 `--lang zh|en` 切换 CLI 输出语言 / Support bilingual CLI output with `--lang`
7. 不再使用时可删除本地缓存，减少凭证残留 / Clear local cache when no longer needed

## API 调用 / API Usage

使用 Python 脚本查询车况信息：  
Use the Python script to query vehicle information:

```bash
# 查询全部信息
python3 query_vehicle.py

# 使用单一环境变量直接查询
export TIKA_API_KEY='your_full_api_key'
python3 query_vehicle.py
python3 query_vehicle.py --check-auth

# 首次写入认证信息并查询
python3 query_vehicle.py --apikey 'your_full_api_key'

# 仅写入认证信息，不发起查询
python3 query_vehicle.py --apikey 'your_full_api_key' --save-token-only

# 检查当前认证状态
python3 query_vehicle.py --check-auth

# 删除本地认证缓存
python3 query_vehicle.py --clear-auth

# 仅查询车辆位置
python3 query_vehicle.py -p
python3 query_vehicle.py --position

# 仅查询车况信息
python3 query_vehicle.py -c
python3 query_vehicle.py --condition

# 输出原始 JSON 数据
python3 query_vehicle.py --json
python3 query_vehicle.py -p --json
python3 query_vehicle.py -c --json

# 使用英文输出
python3 query_vehicle.py --lang en

```

脚本文件：[query_vehicle.py](./query_vehicle.py)

## 响应字段 / Response Fields

| 字段路径 | 说明 |
|----------|------|
| `data.sn` | 数字钥匙 SN |
| `data.vin` | 车架号 |
| `data.vehiclePosition.longitude/latitude` | GPS 经纬度 |
| `data.vehiclePosition.address` | 地址 |
| `data.vehiclePosition.positionUpdateTime` | 位置更新时间戳（毫秒） |
| `data.vehicleCondition.power` | 电源状态 |
| `data.vehicleCondition.gear` | 档位 |
| `data.vehicleCondition.trunk` | 后备箱状态 |
| `data.vehicleCondition.door.*` | 车门状态 |
| `data.vehicleCondition.lock.*` | 车锁状态 |
| `data.vehicleCondition.window.*` | 车窗状态 |
| `data.vehicleCondition.airConditionerState.*` | 空调温度设定 |

## 脚本能力 / Script Capabilities

| 参数 | 简写 | 说明 |
|------|------|------|
| `--position` | `-p` | 仅查询车辆位置信息 |
| `--condition` | `-c` | 仅查询车况信息 |
| `--json` | | 输出纯 JSON 数据 |
| `--apikey` | | 传入完整 API Key，并写入缓存 |
| `--save-token-only` | | 仅保存 API Key 到缓存 |
| `--check-auth` | | 仅检查缓存中的认证信息 |
| `--clear-auth` | | 删除本地认证缓存 |
| `--lang` | | 输出语言，支持 `zh` 和 `en` |
| 无参数 | | 查询全部信息 |

其他特性 / Additional notes:

- 自动从缓存文件读取认证信息 / Read auth from cache automatically
- 支持从环境变量读取认证信息，推荐单一变量 `TIKA_API_KEY` / Support reading auth from environment variables, preferably `TIKA_API_KEY`
- 命令行传 API Key 后自动写缓存 / Save the API key automatically when provided by CLI
- 支持清理本地认证缓存 / Support clearing local auth cache
- 兼容当前接口返回字段和旧字段名 / Support current API fields and legacy field names
- 默认输出终端友好的文本结果 / Default to terminal-friendly text output

## 错误处理 / Error Handling

| 错误类型 | 处理方式 |
|----------|----------|
| 认证信息缺失 | 引导用户提供完整 API Key |
| 认证格式错误 | 提示正确格式 |
| 缓存读写失败 | 返回明确文件错误 |
| API 请求失败 | 返回 HTTP 或接口错误信息 |

## 依赖 / Requirements

- `Python 3.6+`
