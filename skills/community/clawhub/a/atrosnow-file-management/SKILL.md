---
name: atrosnow-file-management
description: >
  elephant-guide 后端文件（图片/附件）上传、下载、管理完整开发指南。
  当用户提到 elephant-guide 项目的文件上传、头像、图片显示、附件管理、filemedia、FileMedia、文件缓存、文件正式入库等场景时触发本技能。
  不适用于 AtroSnow 老项目（.c 后缀接口的项目）。
---

# AtroSnow 文件管理系统（elephant-guide）

## 何时使用

- 为 elephant-guide 后端模块新增图片/附件上传功能
- 前端需要上传文件（头像、产品图、城市封面等）
- 需要在业务保存时将临时文件转为正式文件
- 需要展示/下载已上传的文件
- 需要理解 FileMediaModule 的定义和新增方式

---

## 核心组件速查

| 组件 | 路径 |
|------|------|
| 文件 Controller | `controller/sysBaseData/FileMediaController.java` |
| 文件 Service | `service/sysBaseData/I/IFileMediaService.java` |
| 文件实体 | `entity/sysBaseData/FileMedia.java` |
| 缓存类型枚举 | `definition/sysBaseData/FileCacheType.java` |
| 模块类型枚举 | `definition/sysBaseData/FileMediaModule.java` |
| 文件工具类 | `kit/file/FileKit.java` |
| 文件管理器（文件夹名常量） | `kit/file/FileManager.java` |

---

## 一、文件上传（临时文件）

### 1.1 各端上传接口路径

| 用户类型 | FileCacheType | 接口路径 |
|---------|--------------|---------|
| Staff（员工/后台管理） | 10 | `POST /filemedia/b/saveFileMediaCache` |
| Customer（客户/前台） | 30 | `POST /filemedia/f/saveFileMediaCache` |
| Center（中心） | 20 | `POST /filemedia/c/saveFileMediaCache` |
| Artist（艺术家） | 40 | `POST /filemedia/a/saveFileMediaCache` |

### 1.2 请求参数

```
POST /filemedia/{suffix}/saveFileMediaCache
Content-Type: multipart/form-data

file        -- MultipartFile, 必填, 要上传的文件
userID      -- String, 可选, 操作人ID（可从 Header Authorization 提取）
uploadKey   -- String, 可选, 上传批次标识
groupUUID   -- String, 可选, 文件分组UUID
itemNumber  -- String, 可选, 默认 "1"
```

### 1.3 响应示例

```json
{
  "code": 200,
  "fileUUID": "temp_f3a2b1c4d5e6...",
  "fileMediaID": null,
  "msg": "上传成功"
}
```

**关键返回值是 `fileUUID`**，后续保存正式文件时需要用到。

### 1.4 前端上传示例（管理后台 Staff）

```javascript
// 使用 Element Plus el-upload
const uploadFile = async (file) => {
  const formData = new FormData()
  formData.append('file', file.raw)
  // 注意：不需要包裹 params JSON，直接传独立参数
  formData.append('userID', localStorage.getItem('staffUserID') || '')

  const res = await axios.post('/filemedia/b/saveFileMediaCache', formData, {
    headers: { 'Content-Type': 'multipart/form-data' }
  })

  if (res.data.code === 200) {
    return res.data.fileUUID  // 返回临时文件UUID
  }
  throw new Error(res.data.msg || '上传失败')
}
```

---

## 二、图片/文件下载与展示

### 2.1 下载接口（所有端通用）

```
GET /filemedia/{suffix}/downloadFileMedia
```

| 参数 | 类型 | 说明 |
|------|------|------|
| fileMediaID | String | 正式文件ID（正式文件才有） |
| fileUUID | String | 临时文件UUID（临时文件用，缓存文件） |
| imageLevel | String | 图片规格：0=原图, 1=缩略图, 2=中等图 |
| userID | String | 可选 |

**优先级**：`fileMediaID` > `fileUUID`

### 2.2 前端展示图片

```vue
<template>
  <!-- 方式1：直接拼接接口地址（推荐用于正式文件） -->
  <el-image
    :src="`/filemedia/b/downloadFileMedia?fileMediaID=${fileMediaID}&imageLevel=1`"
    fit="cover"
  />

  <!-- 方式2：临时文件（上传后未正式入库前） -->
  <el-image
    :src="`/filemedia/b/downloadFileMedia?fileUUID=${fileUUID}&imageLevel=1`"
    fit="cover"
  />
</template>
```

### 2.3 imageLevel 规格说明

| imageLevel | 含义 |
|-----------|------|
| 0 | 原图 |
| 1 | 缩略图（小） |
| 2 | 中等图 |

---

## 三、文件正式入库（业务服务内调用 createFileMedia）

**核心原则**：不要在 Controller 层调用文件入库，应在业务 Service 保存业务数据时，调用 `IFileMediaService.createFileMedia()`，在回调中把生成的 `fileMediaID` 写入引用该文件的业务表或中间表。

### 3.1 两种 createFileMedia 签名

**签名一：单文件（传入 File 对象）**
```java
int createFileMedia(
    File cacheFile,                    // 缓存目录中的临时文件（File对象）
    FileMediaModule module,            // 模块类型枚举
    int userType,                      // FileCacheType 值（10/20/30/40）
    String sysUserID,                  // 操作人ID
    HashMap<String, Object> responseMap,
    FileMediaCreateCallback callback    // 回调，savingFileMedia(fileMediaId, fileMedia)
)
```

**签名二：批量（传入 fileUUID 列表）**
```java
int createFileMedia(
    int fileCacheType,                 // FileCacheType 值（10/20/30/40）
    List<FileMediaCreateInfor> infos,  // 包含 fileUUID 和 module 信息
    String sysUserID,
    HashMap<String, Object> responseMap,
    FileMediaListCreateCallback callback  // 回调，savingFileMediaList(List<FileMediaCreateInfor>)
)
```

### 3.2 回调接口

```java
// 单文件回调
public interface FileMediaCreateCallback {
    void savingFileMedia(String fileMediaId, FileMedia fileMedia);
}

// 批量回调
public interface FileMediaListCreateCallback {
    void savingFileMediaList(List<FileMediaCreateInfor> infos);
}
```

### 3.3 业务保存流程示例

```java
// 在业务 Service 的保存方法内，调用 createFileMedia 并在回调中关联 fileMediaID

@Autowired
private IFileMediaService fileMediaService;

public void saveCityWithCover(Map<String, String> params, String staffUserID) {
    String cityID = params.get("cityID");
    String fileUUID = params.get("fileUUID");  // 前端传入的临时文件UUID

    City city = cityDAO.findById(cityID);
    city.setName(params.get("name"));

    if (fileUUID != null && !fileUUID.isEmpty()) {
        // 1. 准备入库信息
        FileMediaCreateInfor info = new FileMediaCreateInfor();
        info.setFileUUID(fileUUID);
        info.setModule(FileMediaModule.CITY_COVER);  // 使用模块枚举

        List<FileMediaCreateInfor> infos = new ArrayList<>();
        infos.add(info);

        HashMap<String, Object> responseMap = new HashMap<>();

        // 2. 调用 createFileMedia，在回调中完成关联
        fileMediaService.createFileMedia(
            FileCacheType.FILE_CACHE_TYPE_STAFF,  // 10，员工类型
            infos,
            staffUserID,
            responseMap,
            new FileMediaListCreateCallback() {
                @Override
                public void savingFileMediaList(List<FileMediaCreateInfor> savedInfos) {
                    // 3. 回调中：fileMediaID 已生成，写入业务表
                    for (FileMediaCreateInfor saved : savedInfos) {
                        city.setCoverFileMediaID(saved.getOriginalFileMediaId());
                        city.setUpdateTime(new Date());
                        city.setUpdateUID(staffUserID);
                        cityDAO.update(city);
                    }
                }
            }
        );
    } else {
        cityDAO.save(city);
    }
}
```

### 3.4 另一种方式：单文件直接传 File 对象

如果临时文件已从缓存中取出为 File 对象，可用签名一：

```java
// 先获取临时文件
File cacheFile = new File(fileMediaService.getCacheFilePath(fileUUID, FileCacheType.FILE_CACHE_TYPE_STAFF));

fileMediaService.createFileMedia(
    cacheFile,
    FileMediaModule.CITY_COVER,
    FileCacheType.FILE_CACHE_TYPE_STAFF,
    staffUserID,
    responseMap,
    (fileMediaId, fileMedia) -> {
        // 在回调中关联
        city.setCoverFileMediaID(fileMediaId);
        cityDAO.update(city);
    }
);
```

### 3.5 saveFileMediaFile 接口（文件管理后台专用）

`/filemedia/b/saveFileMediaFile` 是文件管理模块自己用的异步批量入库接口，不适合在业务 Service 中使用。它通过 `saveFileKey` 轮询进度，返回 `fileMediaID`，属于另一种独立流程。

---

## 四、FileMediaModule 模块定义

### 4.1 已有模块

| 枚举名 | value | folder | prefix | 说明 |
|--------|-------|--------|--------|------|
| SYSTEM | 10 | system | SCB | 系统文件 |
| STAFF_USER_HEAD | 20 | staffUser | SHP | 用户头像 |
| CUSTOMER_USER_HEAD | 30 | customerUser | CHP | 客户头像 |
| SHOP_PRODUCT | 40 | shopProduct | SPD | 产品文件 |
| CITY_COVER | 50 | cityCover | CVP | 城市封面图 |
| ART_FILE | 60 | artFile | ATF | 作品图 |
| CENTER_FILE | 70 | centerFile | CHF | 门店资质附件 |
| ARTIST_USER_HEAD | 80 | artistUser | AHP | 创作者头像 |
| APP_FILE | 90 | appFile | APF | APP文件 |

### 4.2 新增模块步骤

在 `FileMediaModule` 枚举中添加新枚举值，需设置4个属性：

```java
// 1. value — 模块值，10的整数倍，项目内不重复
// 2. folder — 临时文件保存的文件夹名（对应 FileManager 中的 FOLD_NAME_XXX）
// 3. prefix — 文件名前缀，3个大写字母，项目内唯一
// 4. description — 模块描述
```

同时在 `FileManager` 中添加文件夹名常量。

---

## 五、FileCacheType 值定义

```java
public class FileCacheType {
    public static final int FILE_CACHE_TYPE_STAFF = 10;    // 员工/后台
    public static final int FILE_CACHE_TYPE_CENTER = 20;   // 中心
    public static final int FILE_CACHE_TYPE_CUSTOMER = 30; // 客户
    public static final int FILE_CACHE_TYPE_ARTIST = 40;   // 艺术家
}
```

---

## 六、常见错误排查

| 错误现象 | 可能原因 |
|---------|---------|
| 405 Method Not Allowed | 接口路径错误，检查是否多了 `.c` 后缀 |
| 文件上传返回 fileUUID=null | file 参数名不对，必须是 `file` |
| 下载图片是空白/404 | fileUUID 临时文件已过期（24h），需重新上传 |
| 图片显示不完整 | imageLevel 设为 0 试试是否为原图 |
| 正式入库失败 | fileUUID 已被使用或已过期 |

---

## 七、完整开发流程

```
1. 前端上传文件
   POST /filemedia/b/saveFileMediaCache
   → 获得 fileUUID

2. 前端提交业务表单（fileUUID + 业务数据）
   POST /xxx/b/saveXXX

3. 后端保存业务数据，同时将 fileUUID 转为正式文件
   POST /filemedia/b/saveFileMediaFile
   → 获得 fileMediaID

4. 前端展示图片
   GET /filemedia/b/downloadFileMedia?fileMediaID=${fileMediaID}&imageLevel=1
```

---

## 八、开发检查清单

- [ ] 确认使用正确的用户类型端（/b/ /f/ /c/ /a/）
- [ ] 上传接口直接传 `file` 参数，不要包裹 JSON
- [ ] fileUUID 有效期 24 小时，及时完成正式入库
- [ ] 图片展示用 downloadFileMedia 接口，不要自己写 Controller
- [ ] 新增 FileMediaModule 时同时更新 FileManager 常量
- [ ] FileCacheType 值用 10/20/30/40，不是 1/2/3/4
