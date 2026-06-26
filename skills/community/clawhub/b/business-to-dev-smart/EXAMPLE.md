# 使用示例

## 示例 1: 首次使用（项目分析）

### 用户输入
```
帮我理解这个项目：~/projects/skye-oms
```

### AI 执行
```
🔍 正在分析项目结构...

📁 发现项目结构：
  ├─ skye-oms-vue/          # Vue3 前端项目
  ├─ skye-wms-java/         # Java 后端项目
  └─ README.md

🔧 技术栈识别：
  前端: Vue3 + Element Plus + Vite
  后端: Java + Spring Boot + MyBatis

📊 架构分析：
  - B端管理系统（订单管理 OMS）
  - 模块化组织（order/inventory/customer）
  - RESTful API 设计
  - 分层后端架构

💾 项目记忆已保存到 ~/projects/skye-oms/.ai-memory/project-profile.md

【项目概述】
这是一个电商订单管理系统（OMS），采用前后端分离架构...

【主要模块】
- 订单管理（order）
- 库存管理（inventory）
- 客户管理（customer）
...
```

---

## 示例 2: 需求分析

### 用户输入
```
分析需求：
业务：客户希望在订单列表增加批量导出功能，可以选择时间范围和状态筛选后导出 Excel。
截图：~/screenshots/order-export.png
```

### AI 执行

**Step 1: 读取项目记忆**
```
💾 读取项目记忆: skye-oms
技术栈: Vue3 + Element Plus + Java Spring Boot
模块: order/inventory/customer
```

**Step 2: 分析需求**
```
🎯 需求理解：
- 功能：订单批量导出
- 筛选条件：时间范围、订单状态
- 输出格式：Excel
- 触发位置：订单列表页面
```

**Step 3: 查找参考代码**
```
🔍 在代码库中查找：

✓ 找到列表页面：
  skye-oms-vue/src/views/order/IndexView.vue
  - 使用 el-table，已有选择框功能
  - 工具栏有导出按钮（单个订单）

✓ 找到导出工具：
  skye-oms-vue/src/utils/exportUtil.ts
  - exportExcel() 函数已实现

✓ 找到 API 模式：
  skye-oms-vue/src/api/order.ts
  - 使用 createAxios 封装
```

**Step 4: 生成文档**
```markdown
# 订单批量导出功能 研发需求文档

## 1. 需求概述
在订单列表页面增加批量导出功能，支持按时间范围和状态筛选后导出 Excel。

## 2. 功能需求
### 2.1 筛选条件
- 时间范围：开始日期 ~ 结束日期
- 订单状态：多选（待处理、已发货、已完成等）

### 2.2 导出流程
1. 用户在订单列表选择记录（复选框）
2. 点击"批量导出"按钮
3. 弹出确认对话框，显示选中数量
4. 确认后下载 Excel 文件

## 3. 页面设计
```html
<!-- 工具栏新增按钮 -->
<div class="toolbar">
  <el-button type="primary" @click="handleBatchExport">
    <el-icon><Download /></el-icon>
    批量导出
  </el-button>
</div>

<!-- 表格添加选择列 -->
<el-table @selection-change="handleSelectionChange">
  <el-table-column type="selection" width="55" />
  <!-- 其他列 -->
</el-table>
```

## 4. 接口设计
### POST /api/order/batchExport
Request:
```json
{
  "orderIds": [1, 2, 3],
  "startDate": "2024-01-01",
  "endDate": "2024-12-31",
  "statusList": ["pending", "shipped"]
}
```

Response:
```
Content-Type: application/vnd.ms-excel
Content-Disposition: attachment; filename=orders.xlsx
```

## 5. 实现参考
### 前端代码参考
**文件**: `src/views/order/IndexView.vue`
```typescript
// 已有功能参考（第 45-78 行）
const handleSelectionChange = (selection: Order[]) => {
  selectedOrders.value = selection
}

// 新增批量导出方法
const handleBatchExport = async () => {
  if (selectedOrders.value.length === 0) {
    ElMessage.warning('请至少选择一条记录')
    return
  }
  // 调用 API...
}
```

**复用工具函数**:
```typescript
// src/utils/exportUtil.ts（已存在）
import { exportExcel } from '@/utils/exportUtil'

exportExcel(response.data, '订单列表.xlsx')
```

### 后端代码参考
**Controller**: 参考 `OrderController.java` 第 34-56 行
**Service**: 参考 `OrderService.java` 的 `getOrderList` 方法

### 建议实现步骤
1. 前端：在 IndexView.vue 工具栏添加按钮（参考现有导出按钮）
2. 后端：OrderController 添加 batchExport 接口
3. 复用现有的 exportExcel 工具函数
4. 测试：验证筛选条件和导出数据正确性

## 6. 开发任务
- [ ] 前端：IndexView.vue 添加批量导出按钮（2h）
- [ ] 后端：OrderController 添加接口（2h）
- [ ] 后端：OrderService 实现导出逻辑（3h）
- [ ] 联调：前后端对接（1h）
```

---

## 示例 3: 复杂需求

### 用户输入
```
业务：我们要做一个新的"库存预警"功能。
当库存低于安全库存时，系统自动发送通知给采购人员，
并在后台生成补货建议。截图在 ~/screenshots/inventory-alert.png
```

### AI 输出关键部分

```markdown
## 6. 实现参考

基于项目代码库分析，建议参考以下实现：

### 定时任务参考
**文件**: `skye-wms-java/src/main/java/com/skye/job/InventoryCheckJob.java`
（假设存在，或参考类似定时任务实现）

```java
// 建议实现：每小时检查一次库存
@Scheduled(cron = "0 0 * * * ?")
public void checkInventoryAlert() {
    // 查询低于安全库存的商品
    // 发送通知
    // 生成补货建议
}
```

### 通知发送参考
**文件**: `skye-wms-java/src/main/java/com/skye/service/NotificationService.java`
```java
// 参考现有的通知发送方式
// 可能支持：站内信、邮件、企业微信等
```

### 前端页面参考
**文件**: `skye-oms-vue/src/views/inventory/IndexView.vue`
```vue
<!-- 在库存列表页面添加预警标识 -->
<el-table-column label="库存状态">
  <template #default="{ row }">
    <el-tag v-if="row.quantity < row.safeStock" type="danger">
      库存不足
    </el-tag>
  </template>
</el-table-column>
```

## 数据库设计
### 新增表：inventory_alert
```sql
-- 参考现有表命名规范
CREATE TABLE inventory_alert (
    id BIGINT PRIMARY KEY AUTO_INCREMENT,
    product_id BIGINT NOT NULL,
    current_quantity INT NOT NULL,
    safe_stock INT NOT NULL,
    alert_type VARCHAR(20), -- 'LOW_STOCK', 'OUT_OF_STOCK'
    status VARCHAR(20), -- 'PENDING', 'NOTIFIED', 'RESOLVED'
    created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
    -- ... 其他字段
);
```

## 任务拆分
- [ ] 数据库：设计库存预警相关表（1h）
- [ ] 后端：库存检查定时任务（4h）
- [ ] 后端：通知发送服务（3h）
- [ ] 后端：补货建议生成算法（4h）
- [ ] 前端：库存预警列表页面（4h）
- [ ] 前端：预警标识和提醒（2h）
- [ ] 测试：全流程验证（2h）
```

---

## 总结

这个 Skill 的核心价值：

1. **AI 像资深工程师一样理解项目** - 不只是读代码，而是理解架构和模式
2. **自动关联需求和代码** - 知道这个功能该参考哪里的实现
3. **生成可执行的文档** - 不只是描述，还告诉开发者具体怎么改

适合场景：
- ✅ 产品经理写需求时，需要技术实现参考
- ✅ 新成员快速理解项目，接手功能开发
- ✅ 外包项目，需要清晰的研发文档
- ✅ 复杂需求，需要梳理实现思路
