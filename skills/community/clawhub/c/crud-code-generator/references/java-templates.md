# Java 代码模板参考

> 所有模板中的 `XxxYyy` 需要替换为实际类名（大写驼峰），`xxxYyy` 替换为小写驼峰，`xxx-yyy` 替换为中划线分隔，`表中文字名` 替换为表 COMMENT 注释。

---

## 1. Entity 模板

**路径**: `ces-domain/src/main/java/com/infypower/fycev/domain/XxxYyy.java`

```java
package com.infypower.fycev.domain;

import cn.hutool.core.bean.BeanUtil;
import cn.hutool.core.bean.copier.CopyOptions;
import com.baomidou.mybatisplus.annotation.*;
import com.gitee.coadmin.base.BaseEntity;
import io.swagger.annotations.ApiModelProperty;
import lombok.Getter;
import lombok.NoArgsConstructor;
import lombok.Setter;

import java.util.Objects;

@Getter
@Setter
@NoArgsConstructor
@TableName("ces_xxx_yyy")
public class XxxYyy extends BaseEntity {
    private static final long serialVersionUID = 1L;

    @ApiModelProperty("主键")
    @TableId(type = IdType.ASSIGN_ID)
    @TableField(fill = FieldFill.INSERT)
    private Long id;

    // === 根据 DDL 字段生成 ===
    // VARCHAR / 必填字段
    @ApiModelProperty("字段注释")
    private String fieldName;

    // BIGINT (非ID)
    @ApiModelProperty("字段注释")
    private Long someId;

    // TINYINT -> 枚举
    @ApiModelProperty("字段注释")
    private XxxStatusEnum status;

    // TINYINT -> Boolean (仅0/1场景)
    @ApiModelProperty("字段注释")
    private Boolean enabled;

    // DATETIME
    @ApiModelProperty("字段注释")
    private java.util.Date someTime;

    // DECIMAL
    @ApiModelProperty("字段注释")
    private java.math.BigDecimal amount;

    // JSON -> String
    @ApiModelProperty("字段注释")
    private String configJson;

    // 逻辑删除字段（仅当 DDL 包含 deleted 字段时添加）
    @ApiModelProperty("逻辑删除：0=未删除, 1=已删除")
    @TableLogic
    private Integer deleted;

    // === 审计字段 ===
    @ApiModelProperty("创建时间")
    @TableField(fill = FieldFill.INSERT)
    private java.util.Date createTime;

    @ApiModelProperty("更新时间")
    @TableField(fill = FieldFill.UPDATE)
    private java.util.Date updateTime;

    @ApiModelProperty("创建人")
    @TableField(fill = FieldFill.INSERT)
    private Long createUser;

    @ApiModelProperty("更新人")
    @TableField(fill = FieldFill.UPDATE)
    private Long updateUser;

    // === 通用方法 ===
    @Override
    public boolean equals(Object o) {
        if (this == o) return true;
        if (o == null || getClass() != o.getClass()) return false;
        return Objects.equals(id, ((XxxYyy) o).id);
    }

    @Override
    public int hashCode() {
        return Objects.hashCode(id);
    }

    public void copyFrom(XxxYyy source) {
        BeanUtil.copyProperties(source, this, CopyOptions.create().setIgnoreNullValue(true));
    }
}
```

**审计字段规则**:
- `id`: `@TableId(type = IdType.ASSIGN_ID)` + `@TableField(fill = FieldFill.INSERT)`
- `createTime` / `createUser`: `@TableField(fill = FieldFill.INSERT)`
- `updateTime` / `updateUser`: `@TableField(fill = FieldFill.UPDATE)`

---

## 2. DTO 模板

**路径**: `ces-domain/src/main/java/com/infypower/fycev/service/dto/XxxYyyDTO.java`

```java
package com.infypower.fycev.service.dto;

import cn.afterturn.easypoi.excel.annotation.Excel;
import com.fasterxml.jackson.annotation.JsonInclude;
import com.fasterxml.jackson.databind.annotation.JsonSerialize;
import com.fasterxml.jackson.databind.ser.std.ToStringSerializer;
import com.gitee.coadmin.base.BaseDto;
import io.swagger.annotations.ApiModelProperty;
import lombok.Getter;
import lombok.NoArgsConstructor;
import lombok.Setter;

import javax.validation.constraints.NotBlank;
import javax.validation.constraints.NotNull;
import javax.validation.constraints.Size;
import java.util.Objects;

@Getter
@Setter
@NoArgsConstructor
@JsonInclude(JsonInclude.Include.NON_NULL)
public class XxxYyyDTO extends BaseDto {
    private static final long serialVersionUID = 1L;

    // Excel 导出后缀常量（在文件顶部或单独常量类定义）
    private static final String SUFFIX = "xxx_yyy_";

    @JsonSerialize(using = ToStringSerializer.class)
    @ApiModelProperty("主键")
    private Long id;

    @JsonSerialize(using = ToStringSerializer.class)
    @NotNull
    @ApiModelProperty("运营商ID")
    private Long operatorId;

    // String 类型 + 校验
    @NotBlank
    @Size(max = 250, message = "备注字数不大于250")
    @ApiModelProperty("备注")
    @Excel(name = "备注", suffix = SUFFIX)
    private String remarks;

    // Long 类型非 ID
    @JsonSerialize(using = ToStringSerializer.class)
    @NotNull
    @ApiModelProperty("关联ID")
    private Long relatedId;

    // Enum 类型
    @NotNull
    @ApiModelProperty("状态")
    @Excel(name = "状态", enumExportField = "desc")
    private XxxStatusEnum status;

    // Boolean 类型
    @Excel(name = "是否启用", suffix = SUFFIX, replace = {"是_true", "否_false", "否_null"})
    private Boolean enabled;

    // Date 类型
    @ApiModelProperty("时间")
    @Excel(name = "时间", format = "yyyy-MM-dd HH:mm:ss", suffix = SUFFIX)
    private java.util.Date someTime;

    @Override
    public boolean equals(Object o) {
        if (this == o) return true;
        if (o == null || getClass() != o.getClass()) return false;
        return Objects.equals(id, ((XxxYyyDTO) o).id);
    }

    @Override
    public int hashCode() {
        return Objects.hashCode(id);
    }
}
```

**@Excel 注解要点**:
- `name`: Excel 列名
- `suffix`: 模板文件标识后缀
- `format`: 日期格式 `"yyyy-MM-dd HH:mm:ss"`
- `replace`: Boolean 替换 `{"是_true", "否_false", "否_null"}`
- `enumExportField`: 枚举字段用 `"desc"` 导出描述文本

---

## 3. QueryParam 模板

**路径**: `ces-domain/src/main/java/com/infypower/fycev/service/dto/XxxYyyQueryParam.java`

```java
package com.infypower.fycev.service.dto;

import com.gitee.coadmin.annotation.Query;
import com.gitee.coadmin.base.BaseQueryParam;
// 注意：如果 QueryParam 中引用了枚举类型，需要添加对应 import
// import com.infypower.enums.XxxStatusEnum;
import lombok.Getter;
import lombok.Setter;

@Getter
@Setter
public class XxxYyyQueryParam extends BaseQueryParam {
    private static final long serialVersionUID = 1L;

    // 精确匹配
    @Query
    private Long operatorId;

    // LIKE 模糊查询
    @Query(type = Query.Type.INNER_LIKE)
    private String name;

    // 大于等于（时间范围下限）
    @Query(type = Query.Type.GREATER_THAN_EQ)
    private java.util.Date createTimeGe;

    // 小于等于（时间范围上限）
    @Query(type = Query.Type.LESS_THAN_EQ)
    private java.util.Date createTimeLe;

    // BETWEEN（时间范围）
    @Query(type = Query.Type.BETWEEN, propName = "createTime")
    private java.util.Date[] createTimeBetween;

    // 精确匹配（状态/类型）
    @Query
    private Boolean status;
}
```

**@Query 类型说明**:

| 类型 | 说明 | 示例 |
|------|------|------|
| 默认（无 type） | 精确匹配 `=` | `@Query` on `Long operatorId` |
| `INNER_LIKE` | 模糊匹配 `LIKE '%?%'` | `@Query(type = INNER_LIKE)` on `String name` |
| `GREATER_THAN_EQ` | `>=` | `@Query(type = GREATER_THAN_EQ)` on `Date createTimeGe` |
| `LESS_THAN_EQ` | `<=` | `@Query(type = LESS_THAN_EQ)` on `Date createTimeLe` |
| `BETWEEN` | 范围查询，需 `propName` 指定原字段 | `@Query(type = BETWEEN, propName = "createTime")` |

---

## 4. Mapper 接口模板

**路径**: `ces-core/src/main/java/com/infypower/fycev/service/mapper/XxxYyyMapper.java`

```java
package com.infypower.fycev.service.mapper;

import com.gitee.coadmin.base.CommonMapper;
import com.infypower.fycev.domain.XxxYyy;
import org.springframework.stereotype.Repository;

@Repository
public interface XxxYyyMapper extends CommonMapper<XxxYyy> {

}
```

---

## 5. Mapper XML 模板

**路径**: `ces-core/src/main/resources/mapper/XxxYyyMapper.xml`

```xml
<?xml version="1.0" encoding="UTF-8"?>
<!DOCTYPE mapper PUBLIC "-//mybatis.org//DTD Mapper 3.0//EN" "http://mybatis.org/dtd/mybatis-3-mapper.dtd">
<mapper namespace="com.infypower.fycev.service.mapper.XxxYyyMapper">

</mapper>
```

---

## 6. Converter 模板

**路径**: `ces-core/src/main/java/com/infypower/fycev/service/converter/XxxYyyConverter.java`

```java
package com.infypower.fycev.service.converter;

import com.baomidou.mybatisplus.core.metadata.IPage;
import com.gitee.coadmin.base.PageInfo;
import com.infypower.fycev.domain.XxxYyy;
import com.infypower.fycev.service.dto.XxxYyyDTO;
import org.mapstruct.Mapper;
import org.mapstruct.ReportingPolicy;

import java.util.List;

@Mapper(componentModel = "spring", unmappedTargetPolicy = ReportingPolicy.IGNORE)
public interface XxxYyyConverter {
    /** DTO转Entity */
    XxxYyy toEntity(XxxYyyDTO dto);

    /** Entity转DTO */
    XxxYyyDTO toDto(XxxYyy entity);

    /** DTO集合转Entity集合 */
    List<XxxYyy> toEntity(List<XxxYyyDTO> dtoList);

    /** Entity集合转DTO集合 */
    List<XxxYyyDTO> toDto(List<XxxYyy> entityList);

    default PageInfo<XxxYyyDTO> convertPage(IPage<XxxYyy> page) {
        if (page == null) return null;
        PageInfo<XxxYyyDTO> pageInfo = new PageInfo<>();
        pageInfo.setTotalElements(page.getTotal());
        pageInfo.setContent(toDto(page.getRecords()));
        return pageInfo;
    }
}
```

---

## 7. Service 接口模板

**路径**: `ces-core/src/main/java/com/infypower/fycev/service/XxxYyyService.java`

```java
package com.infypower.fycev.service;

import com.gitee.coadmin.base.PageInfo;
import com.infypower.fycev.service.dto.XxxYyyDTO;
import com.infypower.fycev.service.dto.XxxYyyQueryParam;
import org.springframework.data.domain.Pageable;

import java.util.List;
import java.util.Set;

/**
 * 表中文字名
 *
 * @author auto-generated
 */
public interface XxxYyyService {

    String CACHE_KEY = "ces:xxxYyy";

    PageInfo<XxxYyyDTO> pageByQueryParam(XxxYyyQueryParam query, Pageable pageable);

    List<XxxYyyDTO> listByQueryParam(XxxYyyQueryParam query);

    long countByQueryParam(XxxYyyQueryParam query);

    XxxYyyDTO getById(Long id);

    void insert(XxxYyyDTO res);

    void updateById(XxxYyyDTO res);

    void removeByIds(Set<Long> ids);
}
```

---

## 8. ServiceImpl 模板

**路径**: `ces-core/src/main/java/com/infypower/fycev/service/impl/XxxYyyServiceImpl.java`

```java
package com.infypower.fycev.service.impl;

import com.baomidou.mybatisplus.core.metadata.IPage;
import com.gitee.coadmin.base.PageInfo;
import com.gitee.coadmin.utils.PageUtil;
import com.gitee.coadmin.utils.QueryHelpMybatisPlus;
import com.infypower.fycev.domain.XxxYyy;
import com.infypower.fycev.service.XxxYyyService;
import com.infypower.fycev.service.converter.XxxYyyConverter;
import com.infypower.fycev.service.dto.XxxYyyDTO;
import com.infypower.fycev.service.dto.XxxYyyQueryParam;
import com.infypower.fycev.service.mapper.XxxYyyMapper;
import lombok.RequiredArgsConstructor;
import lombok.extern.slf4j.Slf4j;
import org.springframework.context.annotation.Lazy;
import org.springframework.data.domain.Pageable;
import org.springframework.stereotype.Service;
import org.springframework.transaction.annotation.Transactional;

import java.util.List;
import java.util.Set;

/**
 * 表中文字名
 *
 * @author auto-generated
 */
@Service
@Slf4j
@RequiredArgsConstructor(onConstructor_ = {@Lazy})
// @CacheConfig(cacheNames = XxxYyyService.CACHE_KEY)
public class XxxYyyServiceImpl implements XxxYyyService {

    private final XxxYyyMapper xxxYyyMapper;
    private final XxxYyyConverter xxxYyyConverter;

    @Override
    public PageInfo<XxxYyyDTO> pageByQueryParam(XxxYyyQueryParam query, Pageable pageable) {
        IPage<XxxYyy> queryPage = PageUtil.toMybatisPage(pageable);
        IPage<XxxYyy> page = xxxYyyMapper.selectPage(queryPage, QueryHelpMybatisPlus.getPredicate(query));
        return xxxYyyConverter.convertPage(page);
    }

    @Override
    public List<XxxYyyDTO> listByQueryParam(XxxYyyQueryParam query) {
        return xxxYyyConverter.toDto(xxxYyyMapper.selectList(QueryHelpMybatisPlus.getPredicate(query, "id", false)));
    }

    @Override
    public long countByQueryParam(XxxYyyQueryParam query) {
        return xxxYyyMapper.selectCount(QueryHelpMybatisPlus.getPredicate(query));
    }

    @Override
    // @Cacheable(key = "'id:' + #p0")
    public XxxYyyDTO getById(Long id) {
        return xxxYyyConverter.toDto(xxxYyyMapper.selectById(id));
    }

    @Override
    // @CacheEvict(allEntries = true)
    @Transactional(rollbackFor = Exception.class)
    public void insert(XxxYyyDTO res) {
        XxxYyy entity = xxxYyyConverter.toEntity(res);
        xxxYyyMapper.insert(entity);
        res.setId(entity.getId());
    }

    @Override
    // @CacheEvict(allEntries = true)
    @Transactional(rollbackFor = Exception.class)
    public void updateById(XxxYyyDTO res) {
        XxxYyy entity = xxxYyyConverter.toEntity(res);
        xxxYyyMapper.updateById(entity);
    }

    @Override
    // @CacheEvict(allEntries = true)
    @Transactional(rollbackFor = Exception.class)
    public void removeByIds(Set<Long> ids) {
        xxxYyyMapper.deleteBatchIds(ids);
    }
}
```

**注意**: 如果 DDL 中包含 `operator_id` 租户字段，`insert` 方法中可能需要自动设置当前用户 operatorId：
```java
Long operatorId = SecurityUtils.getCurrentUserOperatorId();
entity.setOperatorId(operatorId);
```

---

## 9. Controller 模板

**路径**: `ces-admin/src/main/java/com/infypower/fycev/rest/XxxYyyController.java`

```java
package com.infypower.fycev.rest;

import com.gitee.coadmin.annotation.UniformAPI;
import com.gitee.coadmin.base.PageInfo;
import com.gitee.coadmin.modules.logging.annotation.Log;
import com.gitee.coadmin.modules.logging.annotation.type.LogActionType;
import com.infypower.fycev.service.XxxYyyService;
import com.infypower.fycev.service.dto.XxxYyyDTO;
import com.infypower.fycev.service.dto.XxxYyyQueryParam;
import io.swagger.annotations.Api;
import io.swagger.annotations.ApiOperation;
import lombok.RequiredArgsConstructor;
import org.springframework.data.domain.Pageable;
import org.springframework.security.access.prepost.PreAuthorize;
import org.springframework.validation.annotation.Validated;
import org.springframework.web.bind.annotation.*;

import javax.servlet.http.HttpServletResponse;
import java.io.IOException;
import java.util.Set;

/**
 * 表中文字名
 *
 * @author auto-generated
 */
@UniformAPI
@RestController
@RequiredArgsConstructor
@Api(tags = "表中文字名")
@RequestMapping("/api/ces/xxx-yyy")
public class XxxYyyController {

    private final XxxYyyService xxxYyyService;

    @GetMapping
    @Log("查询表中文字名")
    @ApiOperation("查询表中文字名")
    @PreAuthorize("@el.check('xxxYyy:list')")
    public PageInfo<XxxYyyDTO> query(XxxYyyQueryParam query, Pageable pageable) {
        return xxxYyyService.pageByQueryParam(query, pageable);
    }

    @PostMapping
    @Log(value = "新增表中文字名", type = LogActionType.ADD)
    @ApiOperation("新增表中文字名")
    @PreAuthorize("@el.check('xxxYyy:add')")
    public void create(@Validated @RequestBody XxxYyyDTO res) {
        xxxYyyService.insert(res);
    }

    @PutMapping
    @Log(value = "修改表中文字名", type = LogActionType.UPDATE)
    @ApiOperation("修改表中文字名")
    @PreAuthorize("@el.check('xxxYyy:edit')")
    public void update(@Validated @RequestBody XxxYyyDTO res) {
        xxxYyyService.updateById(res);
    }

    @DeleteMapping
    @Log(value = "删除表中文字名", type = LogActionType.DELETE)
    @ApiOperation("删除表中文字名")
    @PreAuthorize("@el.check('xxxYyy:del')")
    public void delete(@RequestBody Set<Long> ids) {
        xxxYyyService.removeByIds(ids);
    }

    @GetMapping(value = "/download")
    @Log("导出表中文字名数据")
    @ApiOperation("导出表中文字名数据")
    @UniformAPI(enable = false)
    @PreAuthorize("@el.check('xxxYyy:list')")
    public void download(HttpServletResponse response, XxxYyyQueryParam query) throws IOException {
        Long operatorId = com.gitee.coadmin.utils.SecurityUtils.getCurrentUserOperatorId();
        if (operatorId > 0L) {
            query.setOperatorId(operatorId);
        }
        long count = xxxYyyService.countByQueryParam(query);
        if (count > 50000) {
            throw new com.gitee.coadmin.exception.CoException("导出数据过多(>50000)，请根据条件分批次导出", "Data count too large");
        }
        java.util.List<XxxYyyDTO> list = xxxYyyService.listByQueryParam(query);
        cn.afterturn.easypoi.excel.entity.ExportParams exportParams = new cn.afterturn.easypoi.excel.entity.ExportParams("表中文字名", "Sheet");
        try (org.apache.poi.ss.usermodel.Workbook workbook = cn.afterturn.easypoi.excel.ExcelExportUtil.exportExcel(exportParams, XxxYyyDTO.class, list)) {
            response.setContentType("application/vnd.openxmlformats-officedocument.spreadsheetml.sheet;charset=utf-8");
            response.setHeader("Content-Disposition", "attachment;filename=file.xlsx");
            workbook.write(response.getOutputStream());
        } catch (Exception e) {
            throw new IOException("Export error", e);
        }
    }
}
```

---

## 10. Enum 模板

**路径**: `ces-domain/src/main/java/com/infypower/enums/XxxStatusEnum.java`

如果属于已有枚举（如 `CommonEffectiveStatusEnum`），直接复用不生成。
简单 0/1 状态建议直接用 `Boolean` 类型。

```java
package com.infypower.enums;

import com.alibaba.fastjson.annotation.JSONField;
import com.baomidou.mybatisplus.annotation.EnumValue;
import com.fasterxml.jackson.annotation.JsonCreator;
import com.fasterxml.jackson.annotation.JsonValue;
import lombok.AllArgsConstructor;
import lombok.Getter;

/**
 * 枚举描述
 */
@Getter
@AllArgsConstructor
public enum XxxStatusEnum {

    VALUE1(0, "描述1"),
    VALUE2(1, "描述2");

    @EnumValue
    @JsonValue
    @JSONField
    private final Integer code;
    private final String desc;

    @JsonCreator
    public static XxxStatusEnum create(Integer value) {
        for (XxxStatusEnum e : XxxStatusEnum.values()) {
            if (e.code.equals(value)) return e;
        }
        throw new IllegalArgumentException("No element matches " + value);
    }
}
```
