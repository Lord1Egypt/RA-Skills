# dahua-cloud-open-iot-basic-general-kit 接口支持检查

## 支持情况汇总

| 序号 | 接口名称 | 状态 | 说明 |
|------|----------|------|------|
| 1 | 获取国标设备注册信息 | ✅ 支持 | `get_sip_info()` / `sip-info` |
| 2 | 添加设备 | ✅ 支持 | `add_device()` / `add` |
| 3 | 批量查询设备详细信息 | ✅ 支持 | `list_device_details()` / `details` |
| 4 | 修改设备或通道名称 | ✅ 支持 | `modify_device_name()` |
| 5 | 获取国标码列表 | ✅ 支持 | `list_gb_code()` / `gb-code` |
| 6 | 修改国标设备信息 | ✅ 支持 | `modify_gb_device()` / `modify-gb` |
| 7 | 获取AppAccessToken | ✅ 支持 | 内部 `_get_app_access_token()`，自动调用 |
| 8 | 添加国标设备 | ✅ 支持 | `add_gb_device()` / `add-gb` |
| 9 | 删除设备 | ✅ 支持 | `delete_device()` / `delete` |
| 10 | 获取设备使能开关状态 | ✅ 支持 | `get_ability_status()` / `ability` |
| 11 | 国标设备查询详细信息 | ✅ 支持 | `list_gb_device_details()` / `gb-details` |
| 12 | 修改设备密码 | ✅ 支持 | `modify_dev_code()` |
| 13 | 获取设备在线状态 | ✅ 支持 | `get_device_online()` / `online` |
| 14 | 查询设备绑定状态 | ✅ 支持 | `check_device_bind()` / `bind` |
| 15 | 设备校时 | ✅ 支持 | `set_current_utc()` |
| 16 | 查询设备品类 | ✅ 支持 | `get_category()` / `category` |
| 17 | 设置设备使能开关 | ✅ 支持 | `set_ability_status()` |
| 18 | 验证设备密码 | ✅ 支持 | `verify_device_password()` / `verify` |
| 19 | 查询设备SD卡容量 | ✅ 支持 | `get_sd_card_storage()` |
| 20 | 获取铃声列表 | ✅ 支持 | `list_custom_ring()` |
| 21 | 新增自定义铃声 | ✅ 支持 | `add_custom_ring()` |
| 22 | 获取设备SD卡状态 | ✅ 支持 | `get_sd_card_status()` |
| 23 | 获取设备SD卡列表 | ✅ 支持 | `list_sd_card_storage()` |
| 24 | 删除自定义铃声 | ✅ 支持 | `delete_custom_ring()` |
| 25 | 设置铃声 | ✅ 支持 | `set_custom_ring()` |
| 26 | 格式化设备SD卡 | ✅ 支持 | `format_sd_card()` |
| 27 | 获取设备当前连接的热点信息 | ✅ 支持 | `current_device_wifi()` |
| 28 | 修改设备连接热点 | ✅ 支持 | `control_device_wifi()` |
| 29 | 获取设备周边热点信息 | ✅ 支持 | `wifi_around()` |
| 30 | 获取设备通道信息 | ✅ 支持 | `get_device_channel_info()` / `channels` |
| 31 | 获取sim信号强度 | ✅ 支持 | `get_sim_signal_strength()` |
| 32 | 查询设备列表 | ✅ 支持 | `get_device_list()` / `list` |
| 33 | 图片解密 | ✅ 支持 | `image_decrypt()` |
| 34 | 根据回调配置ID更新设备订阅消息 | ✅ 支持 | `update_subscribe_by_callback_config()` |
| 35 | 添加回调配置 | ✅ 支持 | `add_callback_config()` |
| 36 | 按设备类别获取支持的消息类型 | ✅ 支持 | `get_message_type_page()` |
| 37 | 按设备ID列表订阅消息 | ✅ 支持 | `message_subscribe()` |
| 38 | 按回调配置ID更新回调配置 | ✅ 支持 | `update_callback_config()` |
| 39 | 删除回调配置及相关订阅消息 | ✅ 支持 | `delete_callback_config()` |
| 40 | 按回调配置ID搜索回调配置信息 | ✅ 支持 | `get_callback_config_info()` |
| 41 | 根据回调配置ID搜索已订阅的设备消息 | ✅ 支持 | `get_subscribe_info_by_callback_config()` |
| 42 | 根据设备id查询消息订阅信息 | ✅ 支持 | `get_subscribe_info_by_device()` |
| 43 | 分页获取回调配置ID和回调配置地址 | ✅ 支持 | `get_all_callback_config()` |

## 统计

- **已实现**: 43 个
- **未实现**: 0 个
- **支持率**: 100%

## 新增方法一览

所有 43 个接口均已实现为 `DahuaIoTClient` 方法，可通过 Python SDK 调用。
