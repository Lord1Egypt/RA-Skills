---
name: eframe-skills
description: eframe 框架快速开发技能。基于linlan-eframe框架快速开发后端接口与前端页面。当需要在eframe(SpringBoot+MyBatis+Security, Vue3+Element Plus)上新增业务模块、生成CRUD接口、写前后端代码时使用。功能：(1)新模块端到端开发流程 (2)model/view/api三层代码范式 (3)读写分离Entry/Op约定 (4)module-generator代码生成器 (5)前端api+views范式。
---

# eframe 框架快速开发技能

> 技能版本：v1.0
> 整理日期：2026-09-12
> 框架仓库：https://gitee.com/linlannet/linlan-eframe
> 技术栈：SpringBoot + Security + MyBatis（JAVA 17） / Vue3 + Vite2 + Element Plus + Ant Design Vue + Pinia

## 定位

本技能解决"如何在 eframe 框架上快速新增一个业务模块并端到端跑通"的问题，聚焦"怎么写快"；代码质量审查口径见仓库根目录 `references/`（`eframe-backend-best-practices.md`、`eframe-frontend-best-practices.md`、`code-quality-checklist.md`、`security-checklist.md`）。

所有范式均提取自框架现有代码（数据字典模块 BaseDictionary 全链路），非通用 Spring Boot 建议。

## 1. 框架分层总览

后端按职责拆成 10 个 Maven 模块，包根统一为 `net.linlan`，新增业务代码只落在其中 3 层：

| 模块 | 包路径 | 职责 | 放什么 |
|------|--------|------|--------|
| eframe-model | `net.linlan.sys.{域}.` / `net.linlan.frame.{域}.` | 数据层 | entity、dto、param、dao、service |
| eframe-view | `net.linlan.frame.view.{域}.` | 视图层（读写分离） | vo、voParam、manager、service |
| eframe-api | `net.linlan.frame.api.{域}.` | 接口层 | Controller（继承 BaseController） |

其余模块只读不改：eframe-core（公共基础设施）、eframe-web（应用壳）、eframe-support（工具）、module-generator（生成器）、module-quartz（定时任务）、module-extend（扩展）。

一个数据流单向传递：**Controller(api) → Service(view) → Service(model) → Dao(model)**，禁止跨层反向依赖。

## 2. 新模块快速开发流程（8步）

以新增一个 `{域}/{实体}`（如 `system/dictionary`）为例，按序执行，每步可独立验收：

1. **建表**：在 `scripts/` 下写 DDL，字段命名全大写加下划线；或用 module-generator 直接读库生成。
2. **model层**：写 entity（含 `init()` 方法）+ dto + param（含 `getPage()/getLimit()`）+ dao（MyBatis mapper）+ service（`getPageDto/getDtoById/save/update/deleteByIds`）。
3. **view层**：写 vo（含静态转换器 `DTO`/`INITO` 与 `transTo()`）+ voParam（含 `toModelParam()`），按需加 manager/service 做跨域编排。
4. **api层**：写 Controller，继承 `BaseController`，套用第 3 节范式。
5. **权限接入**：Controller 方法加 `@PreAuthorize("@ss.hasPerms('域:实体:动作')")`。
6. **前端 api**：在 `src/api/{域}/{实体}.js` 写 listData/getData/addData/updateData/delData。
7. **前端 views**：在 `src/views/{域}/{实体}/index.vue` 写页面，配 router 和菜单。
8. **联调验证**：后端 `mvn clean install` 通过、前端 `npm run dev` 跑通、接口返回 `code=200`。

## 3. 后端三层代码范式

完整可复制代码见 `references/backend-layers.md`（字典模块全链路示例）。关键点如下。

### model层 service 范式

```java
@Service
public class XxxService {
    @Resource
    private XxxDao dao;

    public Page<XxxDto> getPageDto(XxxParam param) {
        PageHelper.startPage(param.getPage(), param.getLimit());
        return dao.getPageDto(param);
    }
    public XxxDto getDtoById(Long id) { return dao.getDtoById(id); }
    public void save(Xxx entity) { entity.init(); dao.save(entity); }
    public void update(Xxx entity) { dao.update(entity); }
    public void deleteByIds(Long[] ids) { dao.deleteByIds(ids); }
}
```

### view层 vo/voParam 范式

```java
// vo：定义 DTO 转换函数 + transTo 反向转换
public class XxxVo {
    public static final Function<XxxDto, XxxVo> DTO = ...;   // Dto -> Vo
    public static final Function<XxxDto, XxxVo> INITO = ...; // 简版转换
    public static Xxx transTo(XxxVo input) { ... }           // Vo -> entity
}

// voParam：请求参数，提供 toModelParam 转 model 层 param
public class XxxVoParam {
    public XxxParam toModelParam() { ... }
}
```

### api层 Controller 范式

```java
@RestController
@RequestMapping("/api/{域}/")
public class XxxController extends BaseController {
    @Resource private XxxService xxxService;      // model层 service
    @Resource private FrameXxxService frameXxxService; // view层 service（可选）

    @GetMapping("{实体}/list")
    @PreAuthorize("@ss.hasPerms('{域}:{实体}:list')")
    @PlatLog(value = "查询列表")
    @Encrypt
    public ResponseEntity<Pagination<XxxVo>> list(XxxVoParam param) {
        Page<XxxDto> result = xxxService.getPageDto(param.toModelParam());
        List<XxxVo> vos = Lists.transform(result.getResult(), XxxVo.DTO);
        return successPage(vos, result.getPageSize(), result.getPageNum(), result.getTotal());
    }

    @GetMapping("{实体}/{id}")
    @PreAuthorize("@ss.hasPerms('{域}:{实体}:detail')")
    @Encrypt
    public ResponseEntity<XxxVo> getInfo(@PathVariable Long id) {
        return success(XxxVo.DTO.apply(xxxService.getDtoById(id)));
    }

    @PostMapping("{实体}/save")
    @PreAuthorize("@ss.hasPerms('{域}:{实体}:save')")
    @PlatLog(value = "新增")
    @Encrypt
    public ResponseEntity<String> save(@Validated @RequestBody XxxVo input) {
        xxxService.save(XxxVo.transTo(input));
        return success();
    }
}
```

导出接口套用：`ExcelUtil<XxxVo> util = new ExcelUtil<>(XxxVo.class); util.exportExcel(response, vos, "标题");`

## 4. 命名与读写分离约定

- **读写分离（Entry/Op）**：generator 生成的 api 模板分 `EntryApi.java.vm`（读接口）和 `OpApi.java.vm`（写接口），view 层分 `EntryManager`/`OpManager`。读接口（list/detail/tree/export）与写接口（save/update/delete）分离组织。
- **对象后缀**：entity（无后缀或直接业务名）、dto（`XxxDto`）、param（`XxxParam`，model层查询参数）、vo（`XxxVo`，返回视图）、voParam（`XxxVoParam`，接口入参）、dao（`XxxDao`）、service（`XxxService`）。
- **域划分**：api/view 层按 admin / config / monitor / open / sys 分域；model 层按 `sys.{子域}`（如 sys.base、sys.role）分域。
- **URL 规范**：`/api/{域}/{实体}/{动作}`，动作用 list/detail 风格，写操作用 save/update/delete。

## 5. 代码生成器（module-generator）

框架内置 Ruoyi 风格生成器（`GenTable`/`GenTableColumn`），可一键从数据库表生成全链路代码。模板清单（`module-generator/src/main/resources/vm/`）：

- `java/model/`：Entity、Dto、Dao、Service、Param、Controller、SubEntity
- `java/view/`：Vo、EntryManager、OpManager
- `java/controller/`：EntryApi、OpApi
- `vue/`：api.js、index.vue、index-tree.vue（含 v2/v3 版本）
- `sql/`：sql.vm

**优先用生成器**：新表先让生成器产出骨架，再手工补充业务逻辑，比从零手写快一个量级。生成后按第 3 节范式核对占位符是否替换完整。

## 6. 前端开发范式

### api 层（`src/api/{域}/{实体}.js`）

```javascript
import request from '@/utils/request'

export function listData(query) {
    return request({ url: '/api/{域}/{实体}/list', method: 'get', params: query })
}
export function getData(id) {
    return request({ url: '/api/{域}/{实体}/' + id, method: 'get' })
}
export function addData(data) {
    return request({ url: '/api/{域}/{实体}', method: 'post', data: data })
}
export function updateData(data) {
    return request({ url: '/api/{域}/{实体}', method: 'put', data: data })
}
export function delData(id) {
    return request({ url: '/api/{域}/{实体}/' + id, method: 'delete' })
}
```

### 请求封装（`src/utils/request.js`，勿重写）

- axios 实例 baseURL 取 `import.meta.env.VITE_API_DOMAIN`
- token 注入：`Authorization: 'Linlan ' + getToken()`
- 响应码 `code === 200 || code === '0'` 视为成功；401 弹登录过期、500 弹失败通知
- 通用下载用导出的 `download(url, params, filename)`

### views 层（`src/views/{域}/{实体}/index.vue`）

- UI 库用 Element Plus + Ant Design Vue 混用（框架已装两套）
- 状态管理 Pinia + Vuex 并存，新页面优先 Pinia
- 页面配 `src/router/` 路由，菜单由后端 `sys_menu` 表驱动

前端完整代码见 `references/frontend-pattern.md`。

## 7. 关键注解与工具清单

**BaseController 可用方法**（继承即得）：`success()/success(data)/successPage(list,limit,page,total)/successPage(Page)/failure()/empty()/okMsg()/errorMsg()/warn()/returnRow(rows)/returnRow(bool)/redirect()/getLoginUser()/getUserId()/getDeptId()/getOrganId()/getUsername()`，另内置 `@InitBinder`（日期字符串转 Date）与 `@ExceptionHandler`。

**Controller 注解**：`@PlatLog`（操作日志）、`@PreAuthorize("@ss.hasPerms(...)")`（权限）、`@Encrypt`（响应加密）、`@LimitScope`（限流）、`@Validated @RequestBody`（参数校验）。

**model 层注解**（`net.linlan.annotation.*`）：`@DataScope`（数据权限）、`@NoDataScope`、`@AuthIgnore`/`@AuthLogin`、`@Excel`/`@Excels`（导出列）、`@Encrypt`、`@Sensitive`、`@NoSqlFilter`、`@NoXssFilter`、`@OriginalResponse`、`@LimitScope`。

**响应类型**：`net.linlan.commons.core.http.ResponseEntity`（ok/error/warn）、分页 `net.linlan.commons.db.page.Pagination`。

## 8. 开发检查清单

- [ ] DDL 字段命名全大写下划线，含标准字段（状态/创建人/创建时间/更新人/更新时间/删除标志/备注）
- [ ] entity 有 `init()` 方法，save 前调用
- [ ] service 分页用 `PageHelper.startPage(param.getPage(), param.getLimit())`
- [ ] vo 转换器用静态 `DTO`/`INITO` Function + `transTo()`，param 有 `toModelParam()`
- [ ] Controller 继承 BaseController，`@RequestMapping` 前缀 `/api/{域}/`
- [ ] 每个接口方法带 `@PreAuthorize` 权限点 + `@PlatLog` + `@Encrypt`
- [ ] 前端 api 文件用 `@/utils/request`，不重写 axios 实例
- [ ] 生成器产出核对占位符替换完整、无大小写错误

## 核心文件

| 文件 | 用途 |
|------|------|
| `references/backend-layers.md` | 后端三层完整代码范式（字典模块全链路示例） |
| `references/frontend-pattern.md` | 前端 api + request + views 范式 |
