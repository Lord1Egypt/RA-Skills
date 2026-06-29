# 存储与文件

> 官方文档: 数据缓存 API、文件 API

## 本地存储

单个 key 数据上限 **1MB**，总存储上限 **10MB**。

### 同步 API

```javascript
tt.setStorageSync("key", "value");
tt.setStorageSync("userInfo", { name: "test", level: 10 });

var val = tt.getStorageSync("key");
var info = tt.getStorageSync("userInfo");

tt.removeStorageSync("key");
tt.clearStorageSync();

var storageInfo = tt.getStorageInfoSync();
console.log("当前:", storageInfo.currentSize + "KB");
console.log("上限:", storageInfo.limitSize + "KB");
console.log("keys:", storageInfo.keys);
```

### 异步 API

```javascript
// 存储
tt.setStorage({ key: "key", data: "value",
  success: function() {}, fail: function(err) {} });

// 读取
tt.getStorage({ key: "key",
  success: function(res) { console.log(res.data); } });

// 删除
tt.removeStorage({ key: "key" });

// 清空
tt.clearStorage();

// 获取信息
tt.getStorageInfo({
  success: function(res) {
    console.log(res.currentSize, res.limitSize, res.keys);
  }
});
```

## 文件系统 (FileSystemManager)

### tt.getFileSystemManager()

获取全局唯一的文件管理器实例。

```javascript
var fs = tt.getFileSystemManager();
```

### 用户数据目录

```javascript
var userPath = tt.env.USER_DATA_PATH;
// 此目录下可自由读写，其他位置只读
```

### 文件操作

```javascript
// 写文件
fs.writeFile({
  filePath: userPath + "/save.dat",
  data: "save content", // String 或 ArrayBuffer
  encoding: "utf8",
  success: function() {}
});

// 读文件
fs.readFile({
  filePath: userPath + "/data.json",
  encoding: "utf8",
  success: function(res) { var data = JSON.parse(res.data); }
});

// 追加
fs.appendFile({
  filePath: userPath + "/log.txt",
  data: "new line\n",
  encoding: "utf8"
});

// 复制文件
fs.copyFile({
  srcPath: tempFilePath,
  destPath: userPath + "/image.png"
});

// 删除文件
fs.unlink({ filePath: userPath + "/old.dat" });

// 重命名
fs.rename({
  oldPath: userPath + "/old.dat",
  newPath: userPath + "/new.dat"
});

// 获取文件信息
fs.stat({
  path: userPath + "/data.json",
  success: function(res) {
    console.log("大小:", res.stats.size);
    console.log("是文件:", res.stats.isFile());
    console.log("是目录:", res.stats.isDirectory());
    console.log("修改时间:", res.stats.lastModifiedTime);
  }
});

// 检查文件是否存在
fs.access({
  path: userPath + "/data.json",
  success: function() { console.log("文件存在"); },
  fail: function() { console.log("文件不存在"); }
});
```

### 目录操作

```javascript
// 创建目录
fs.mkdir({ dirPath: userPath + "/saves", recursive: true });

// 读取目录内容
fs.readdir({
  dirPath: userPath,
  success: function(res) { console.log("文件列表:", res.files); }
});

// 删除目录
fs.rmdir({ dirPath: userPath + "/saves", recursive: true });
```

### 保存临时文件

```javascript
// 保存临时文件到本地持久化
fs.saveFile({
  tempFilePath: "临时文件路径",
  filePath: userPath + "/persistent.dat", // 可选
  success: function(res) {
    console.log("已保存:", res.savedFilePath);
  }
});

// 获取已保存文件列表
fs.getSavedFileList({
  success: function(res) { console.log("文件列表:", res.fileList); }
});

// 删除已保存文件
fs.removeSavedFile({ filePath: userPath + "/old.dat" });
```

### FileSystemManager 完整方法

| 方法 | 说明 |
|------|------|
| readFile | 读取文件内容 |
| writeFile | 写入文件（覆盖） |
| appendFile | 追加文件内容 |
| copyFile | 复制文件 |
| unlink | 删除文件 |
| rename | 重命名文件/目录 |
| mkdir | 创建目录 |
| rmdir | 删除目录 |
| readdir | 读取目录内容 |
| stat | 获取文件/目录信息 |
| access | 检查文件/目录是否存在 |
| saveFile | 保存临时文件到本地 |
| getSavedFileList | 获取已保存文件列表 |
| removeSavedFile | 删除已保存文件 |
| getFileInfo | 获取文件信息 |

### 路径说明

- 代码包内文件路径以 `/` 开头，为只读
- 用户目录通过 `tt.env.USER_DATA_PATH` 获取，可读写
- 本地临时文件路径不可持久化保存
- 本地用户文件路径以 `ttfile://` 开头
