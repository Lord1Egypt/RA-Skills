# 常见问题 FAQ

## Q1: 设置了环境变量但仍然报错？

**检查步骤**:

1. 是否**重新打开了命令行窗口**？
   - 新打开的窗口才会加载新的环境变量
   - 已打开的窗口不会自动更新

2. 环境变量是否设置正确？
   ```powershell
   # Windows 验证
   $env:DAHUA_CLOUD_PRODUCT_ID
   $env:DAHUA_CLOUD_AK
   # 注意：不要打印 SK，避免泄露
   ```

3. 是否在正确的区域添加？
   - 确保在"用户变量"而非"系统变量"（或统一在同一区域）
   - 变量名必须完全一致（区分大小写）

---

## Q2: 图形界面找不到"环境变量"在哪里？

**快速入口方法**:

### 方法 A: Win + R 快捷键
```
1. 按下 Win + R
2. 输入 sysdm.cpl
3. 点确定
```

### 方法 B: 右键"此电脑"
```
1. 右键"此电脑"
2. 选择"属性"
3. 点击"高级系统设置"
4. 点"环境变量"
```

### 方法 C: 搜索
```
1. 按 Win 键
2. 输入"环境变量"
3. 选择"编辑系统环境变量"
```

---

## Q3: 如何删除已有的环境变量？

**Windows GUI**:
1. 打开"环境变量"设置
2. 在"用户变量"列表中找到对应的变量
3. 选中后点击 **"删除(D)..."**
4. 确认删除

---

## Q4: 可以测试环境变量是否已设置吗？

**Windows**:
```powershell
# 测试单个变量
Get-ChildItem Env: | Where-Object {$_.Name -like "*DAHUA*"}

# 查看所有 Dahua 相关变量
$env:DAHUA_CLOUD_PRODUCT_ID
$env:DAHUA_CLOUD_AK
# 注意：不要打印 SK
```

**Linux/Mac**:
```bash
# 列出所有包含 DAHUA 的环境变量
env | grep DAHUA
```

---

## Q5: 设备添加失败怎么办？

**可能原因**:
- 设备密码加密方式不正确（推荐使用 AES256）
- 设备序列号已存在
- 设备品类编码不正确（如 IPC、NVR）
- 设备未初始化或未设置密码
- 设备未连接网络

**解决方法**:
1. 使用 `encrypt` 子命令验证加密结果：`python dahua_iot_client.py encrypt -p admin123 -s <SK> -d <设备ID> -m aes256`
2. 检查设备是否已在大华云平台注册
3. 确认设备品类编码与设备类型匹配
4. 查看 API 返回的 `msg` 字段了解具体错误

---

## Q6: Token 过期怎么办？

**解决方案**: 客户端会自动管理 Token，在过期前自动刷新，无需手动处理。Token 有效期为 7 天。

---

## Q7: 签名验证失败？

**检查清单**:
- [ ] AccessKey、SecretKey、ProductID 是否正确
- [ ] 环境变量是否正确设置（区分大小写）
- [ ] 是否重新打开了命令行窗口（环境变量需重启终端生效）
- [ ] 系统时间是否同步（签名依赖时间戳）

---

## Q8: 设备离线怎么办？

**可能原因**:
- 设备电源未开启
- 设备网络连接异常
- 设备未正确注册到大华云平台

**解决方法**:
1. 检查设备电源和网络连接
2. 登录大华云平台确认设备状态
3. 调用 `get_device_online` 确认返回的在线状态

---

## Q9: SD 卡格式化失败？

**可能原因**:
- 设备不支持远程格式化
- SD 卡处于读写状态
- 设备离线

**解决方法**:
1. 确认设备支持 `formatSDCard` 能力
2. 调用 `list_device_details` 查看 `deviceAbility` 是否包含 SD 卡相关能力
3. 确保设备在线后再执行

---

## Q10: 如何获取 Cloud 凭证？

1. 登录 [大华云开发者平台](https://open.cloud-dahua.com/)
2. 注册并创建应用
3. 在应用详情页获取：
   - Product ID (AppID)
   - Access Key (AK)
   - Secret Key (SK)

---

## Q11: 支持哪些操作系统？

- ✅ Windows 10/11
- ✅ Linux (Ubuntu/CentOS 等)
- ✅ macOS

---

## Q12: 如何从旧版 sign_helper 迁移？

参考 [SKILL.md](./SKILL.md) 中的「迁移指南」章节，使用 `create_client_from_env()` 替代手动管理 Token 和签名。

---

## Q13: 作为 SDK 集成时如何关闭日志输出？

创建客户端时设置 `verbose=False`：

```python
client = create_client_from_env(verbose=False)
# 或
client = DahuaIoTClient(app_id='...', access_key='...', secret_key='...', verbose=False)
```

---

## Q14: Python 导入 dahua_iot_client 失败？

确保满足以下之一：
1. 在 `scripts/` 目录下运行 Python
2. 将 `scripts/` 加入 `PYTHONPATH`：`export PYTHONPATH="${PYTHONPATH}:$(pwd)/scripts"`
3. 使用 `sys.path.insert(0, 'scripts')` 后再 `import dahua_iot_client`

---

**还有其他问题？** 请查阅 [SKILL.md](./SKILL.md) 获取更详细的技术文档。
