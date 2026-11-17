# eframe 后端三层代码范式

> 本文档为 SKILL.md 的详细代码参考，所有示例提取自框架现有数据字典模块（BaseDictionary）全链路真实代码。

## 一、分层与包路径

```
net.linlan
├── sys.{子域}                     # model层（eframe-model）
│   ├── entity/  Xxx.java          实体（无后缀，业务名）
│   ├── dto/     XxxDto.java       DTO（含 DictionaryInitDto 等派生）
│   ├── param/   XxxParam.java     查询参数（含 getPage/getLimit）
│   ├── dao/     XxxDao.java       MyBatis mapper
│   └── service/ XxxService.java   数据服务
├── frame.{域}                     # model层（eframe-model，admin域）
│   ├── dao/  AdminXxxDao.java
│   └── dto/  AdminXxxDto.java
├── frame.view.{域}                # view层（eframe-view）
│   ├── param/  XxxVoParam.java    接口入参
│   ├── vo/     XxxVo.java         返回视图
│   ├── manager/XxxOpManager.java  编排（读写分离写侧）
│   ├── service/XxxService.java    跨域服务（如 FrameDictionaryService）
│   └── utils/  ExcelUtil.java     导出工具
└── frame.api.{域}                 # api层（eframe-api）
    ├── BaseController.java        公共基类
    └── XxxController.java         控制器
```

## 二、model 层完整范式

### entity（net.linlan.sys.base.entity.BaseDictionary）

实体保存前需调用 `init()` 完成初始化（主键、默认字段等），框架约定：

```java
public class BaseDictionary {
    private Long id;
    private String typeCode;
    private String cddValue;
    private String name;
    private Long parentId;
    // getter/setter 省略

    public void init() {
        // 框架约定：保存前初始化，设置主键/默认值
    }
}
```

### param（net.linlan.sys.base.param.BaseDictionaryParam）

```java
public class BaseDictionaryParam {
    private Integer page;   // 页码
    private Integer limit;  // 每页条数
    private String typeCode;
    // getter/setter 省略
    public Integer getPage() { return page; }
    public Integer getLimit() { return limit; }
}
```

### dao（net.linlan.sys.base.dao.BaseDictionaryDao）

MyBatis mapper，XML 位于 `mapper/net/linlan/sys/base/BaseDictionaryDao.xml`。方法命名约定：

```java
public interface BaseDictionaryDao {
    List<BaseDictionary> getList(Map<String, Object> map);
    BaseDictionary findById(Long id);
    void save(BaseDictionary entity);
    void batchSave(List<BaseDictionary> list);
    void update(BaseDictionary entity);
    void deleteById(Long id);
    void deleteByIds(Long[] ids);
    int getCount(Map<String, Object> map);
    Page<BaseDictionaryDto> getPageDto(BaseDictionaryParam param);
    BaseDictionaryDto getDtoById(Long id);
}
```

### service（net.linlan.sys.base.service.BaseDictionaryService）

```java
@Service
@Slf4j
public class BaseDictionaryService {
    @Resource
    private BaseDictionaryDao dao;
    @Resource
    private RedisService redisService;  // 缓存可选

    public Page<BaseDictionaryDto> getPageDto(BaseDictionaryParam param) {
        PageHelper.startPage(param.getPage(), param.getLimit());
        return dao.getPageDto(param);
    }

    public BaseDictionaryDto getDtoById(Long id) {
        return dao.getDtoById(id);
    }

    public void save(BaseDictionary baseDictionary) {
        baseDictionary.init();          // 保存前必须 init
        dao.save(baseDictionary);
    }

    public void update(BaseDictionary baseDictionary) {
        dao.update(baseDictionary);
    }

    public void deleteByIds(Long[] ids) {
        dao.deleteByIds(ids);
    }
}
```

## 三、view 层完整范式

### vo（net.linlan.frame.view.sys.vo.BaseDictionaryVo）

视图对象用静态 Function 做 DTO 转换，用静态方法做反向转换：

```java
public class BaseDictionaryVo {
    private Long id;
    private String typeCode;
    private String name;

    // Dto -> Vo 完整转换（列表用）
    public static final Function<BaseDictionaryDto, BaseDictionaryVo> DTO = dto -> {
        BaseDictionaryVo vo = new BaseDictionaryVo();
        vo.setId(dto.getId());
        vo.setTypeCode(dto.getTypeCode());
        vo.setName(dto.getName());
        return vo;
    };

    // Dto -> Vo 简版转换（字典初始化用）
    public static final Function<DictionaryInitDto, BaseDictionaryVo> INITO = dto -> {
        BaseDictionaryVo vo = new BaseDictionaryVo();
        vo.setId(dto.getId());
        vo.setName(dto.getName());
        return vo;
    };

    // Vo -> entity 反向转换（保存/更新用）
    public static BaseDictionary transTo(BaseDictionaryVo input) {
        BaseDictionary entity = new BaseDictionary();
        BeanUtils.copyProperties(input, entity);
        return entity;
    }
}
```

### voParam（net.linlan.frame.view.sys.param.BaseDictionaryVoParam）

```java
public class BaseDictionaryVoParam {
    private Integer page;
    private Integer limit;
    private String typeCode;

    // 入参 -> model 层 param
    public BaseDictionaryParam toModelParam() {
        BaseDictionaryParam param = new BaseDictionaryParam();
        param.setPage(page);
        param.setLimit(limit);
        param.setTypeCode(typeCode);
        return param;
    }
}
```

### 跨域服务（net.linlan.frame.view.sys.service.FrameDictionaryService）

view 层服务负责跨 model 服务编排、字典翻译、缓存策略：

```java
@Service
@Slf4j
public class FrameDictionaryService {
    @Resource private RedisService redisService;
    @Resource private BaseDictionaryService baseDictionaryService;
    @Resource private SysRoleService sysRoleService;   // 跨域组合
    // ... 其他服务

    // 字典缓存策略：Redis 2小时 + 内存 1小时 双重缓存
    public List<DictionaryInitDto> getDicList(String typeCode) {
        List<DictionaryInitDto> dist = redisService.getList(BASE_DICTIONARY_KEY + typeCode);
        if (dist != null && dist.size() > 0) {
            return dist;
        }
        List<DictionaryInitDto> dicResult = baseDictionaryService.getInitByTypeCode(typeCode);
        if (dicResult != null && dicResult.size() > 0) {
            redisService.setList(BASE_DICTIONARY_KEY + typeCode, dicResult,
                KernelConstant.ONE_HOUR_EXPIRE * 2);
        }
        return dicResult;
    }

    // 字典翻译：反射调用 getter/setter 完成 code -> name 翻译
    public void translate(List list, Map<String, String> dicMap) {
        for (Object obj : list) { translateObj(obj, dicMap); }
    }
}
```

## 四、api 层完整范式

### BaseController 关键方法（继承即得）

```java
public class BaseController {
    public ResponseEntity success()                              // 成功，data=SUCCESS
    public ResponseEntity success(Object data)                   // 成功，携带数据
    public ResponseEntity successPage(List<?> list, int limit, int page, long total)
    public ResponseEntity successPage(Page page)                 // pagehelper Page
    public ResponseEntity failure()                              // 失败
    public ResponseEntity empty()                                // 空结果（204）
    public ResponseEntity okMsg(String message)
    public ResponseEntity errorMsg(String message)
    public ResponseEntity warn(String message)
    protected ResponseEntity returnRow(int rows)                 // rows>0 成功
    protected ResponseEntity returnRow(boolean result)
    public String redirect(String url)
    public FrameUserDetails getLoginUser()
    public String getUserId() / getDeptId() / getOrganId() / getUsername()
    // 内置 @InitBinder 处理 Date 字符串，@ExceptionHandler 统一异常
}
```

### Controller 完整示例（net.linlan.frame.api.sys.BaseDictionaryController）

```java
@RestController
@RequestMapping("/api/system/")
public class BaseDictionaryController extends BaseController {

    @Resource private BaseDictionaryService baseDictionaryService;   // model层
    @Resource private FrameDictionaryService frameDictionaryService; // view层

    // 列表：param -> model param -> page dto -> 转 vo -> successPage
    @PlatLog(value = "获取数据字典信息列表")
    @PreAuthorize("@ss.hasPerms('system:dictionary:list')")
    @GetMapping("dictionary/list")
    @Encrypt
    public ResponseEntity<Pagination<BaseDictionaryVo>> list(BaseDictionaryVoParam param) {
        if (ObjectUtils.isEmpty(param)) return failure();
        Page<BaseDictionaryDto> result = baseDictionaryService.getPageDto(param.toModelParam());
        if (ObjectUtils.isEmpty(result)) return empty();
        List<BaseDictionaryVo> vos = Lists.transform(result.getResult(), BaseDictionaryVo.DTO);
        return successPage(vos, result.getPageSize(), result.getPageNum(), result.getTotal());
    }

    // 详情
    @GetMapping(value = "dictionary/{dictId}")
    @Encrypt
    public ResponseEntity<BaseDictionaryVo> getInfo(@PathVariable Long dictId) {
        BaseDictionaryDto dto = baseDictionaryService.getDtoById(dictId);
        return success(BaseDictionaryVo.DTO.apply(dto));
    }

    // 新增：@Validated @RequestBody + transTo 反向转换
    @PreAuthorize("@ss.hasPerms('system:dictionary:save')")
    @PlatLog(value = "新增字典", category = 10)
    @PostMapping("dictionary/save")
    @Encrypt
    @LimitScope(name = "baseDictionarySave", key = "baseDictionarySave")
    public ResponseEntity<String> save(@Validated @RequestBody BaseDictionaryVo input) {
        baseDictionaryService.save(BaseDictionaryVo.transTo(input));
        return success();
    }

    // 导出：ExcelUtil 泛型
    @PostMapping("dictionary/export")
    @Encrypt
    public void export(HttpServletResponse response, BaseDictionaryVoParam param) {
        Page<BaseDictionaryDto> result = baseDictionaryService.getPageDto(param.toModelParam());
        List<BaseDictionaryVo> vos = Lists.transform(result.getResult(), BaseDictionaryVo.DTO);
        ExcelUtil<BaseDictionaryVo> util = new ExcelUtil<>(BaseDictionaryVo.class);
        util.exportExcel(response, vos, "字典类型");
    }
}
```

## 五、要点速记

1. **单向依赖**：api -> view -> model，禁止反向。
2. **分页三件套**：`PageHelper.startPage(page, limit)` + `dao.getPageDto(param)` + `successPage(vos, pageSize, pageNum, total)`。
3. **对象转换三件套**：vo 静态 `DTO` Function（列表）、`INITO` Function（简版）、`transTo()`（反向）。param 提供 `toModelParam()`。
4. **保存前 `init()`**：entity 的 save 必经 `entity.init()`。
5. **权限点格式**：`@ss.hasPerms('{域}:{实体}:{动作}')`，动作含 list/detail/save/update/delete/export。
6. **响应加密**：对外接口加 `@Encrypt`，敏感写操作加 `@LimitScope` 限流。
