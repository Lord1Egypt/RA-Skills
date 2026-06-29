# 存储与文件

> 基于官方文档: 存储 API - 数据缓存、PlayerPrefs、文件系统
> 生成时间: 2026-06-24

> ⚠️ **【安全声明】**：
> - **玩家数据**：`Save`/`LoadSaving` 存储的玩家档案包含用户个人信息（昵称、游戏进度等），生产环境禁止打印完整 JSON
> - **PlayerPrefs**：`PlayerPrefs.GetString` 获取的玩家名称等信息禁止打印到生产日志，已用 `#if UNITY_EDITOR || DEVELOPMENT_BUILD` 包裹
> - **文件路径**：避免在生产日志中暴露应用沙盒目录结构

## 一、数据缓存

数据缓存提供轻量级的持久化键值对存储，适合保存游戏设置、玩家偏好、存档摘要等少量结构化数据。底层为异步写入，数据存储在宿主 App 为小游戏分配的专用存储空间中。

### 1.1 TT.Save

**说明**: 保存数据到缓存。以键值对形式持久化字符串数据，支持复杂对象的 JSON 序列化存储。单个 key 对应的 value 建议不超过 1MB。

**语法**:

```csharp
public static void Save(string key, string value)
```

**参数说明**:

| 参数 | 类型 | 必填 | 默认值 | 说明 |
|------|------|------|--------|------|
| key | string | 是 | - | 存储键名，用于后续读取和删除 |
| value | string | 是 | - | 存储的字符串值。建议复杂对象先 JSON 序列化 |

---

### 1.2 TT.LoadSaving

**说明**: 从缓存中读取指定 key 的数据。同步方法，直接返回字符串。若 key 不存在返回空字符串。

**语法**:

```csharp
public static string LoadSaving(string key)
```

**参数说明**:

| 参数 | 类型 | 必填 | 默认值 | 说明 |
|------|------|------|--------|------|
| key | string | 是 | - | 要读取的存储键名 |

**返回值**: `string`，对应存储的值。key 不存在时返回 `""`。

---

### 1.3 TT.DeleteSaving

**说明**: 删除指定 key 的缓存数据。

**语法**:

```csharp
public static void DeleteSaving(string key)
```

**参数说明**:

| 参数 | 类型 | 必填 | 默认值 | 说明 |
|------|------|------|--------|------|
| key | string | 是 | - | 要删除的存储键名 |

---

### 1.4 TT.ClearAllSaving

**说明**: 清空当前小游戏的全部缓存数据。该操作不可逆，调用前应提示用户确认。

**语法**:

```csharp
public static void ClearAllSaving()
```

---

### 1.5 TT.GetSavingDiskSize

**说明**: 获取当前缓存数据占用的磁盘空间大小。同步方法，返回字节数。

**语法**:

```csharp
public static long GetSavingDiskSize()
```

**返回值**: `long`，缓存数据总字节数。

---

### 1.6 代码示例

```csharp
using UnityEngine;
using TT;

/// <summary>
/// 基于数据缓存的存档管理器
/// </summary>
public class SaveManager : MonoBehaviour
{
    private const string SAVE_KEY_PROFILE = "player_profile";
    private const string SAVE_KEY_SETTINGS = "game_settings";
    private const string SAVE_KEY_LEVEL = "level_data";

    /// <summary>
    /// 保存玩家档案（对象序列化存储）
    /// </summary>
    public void SavePlayerProfile(PlayerProfile profile)
    {
        string json = JsonUtility.ToJson(profile);
        TT.Save(SAVE_KEY_PROFILE, json);
        // ⚠️ 安全：玩家档案包含个人信息，禁止打印完整 JSON 到生产日志
        #if UNITY_EDITOR || DEVELOPMENT_BUILD
        Debug.Log($"玩家档案已保存: {json}");
        #else
        Debug.Log("玩家档案已保存");
        #endif
    }

    /// <summary>
    /// 读取玩家档案
    /// </summary>
    public PlayerProfile LoadPlayerProfile()
    {
        string json = TT.LoadSaving(SAVE_KEY_PROFILE);
        if (string.IsNullOrEmpty(json))
        {
            Debug.LogWarning("未找到玩家档案，使用默认值");
            return new PlayerProfile { playerName = "新玩家", level = 1, coins = 100 };
        }

        try
        {
            return JsonUtility.FromJson<PlayerProfile>(json);
        }
        catch (System.Exception e)
        {
            Debug.LogError($"档案解析失败: {e.Message}");
            return new PlayerProfile { playerName = "新玩家", level = 1, coins = 100 };
        }
    }

    /// <summary>
    /// 保存游戏设置
    /// </summary>
    public void SaveSettings(GameSettings settings)
    {
        string json = JsonUtility.ToJson(settings);
        TT.Save(SAVE_KEY_SETTINGS, json);
    }

    /// <summary>
    /// 删除单个存档
    /// </summary>
    public void DeleteSaveData(string key)
    {
        TT.DeleteSaving(key);
        Debug.Log($"已删除存档: {key}");
    }

    /// <summary>
    /// 清空所有存档（⚠️ 不可逆，必须用户确认后执行）
    /// </summary>
    public void ClearAllSaveData()
    {
        // ⚠️ 安全：不可逆操作，调用前必须弹窗获得用户明确确认
        ShowConfirmDialog("确定要清空所有存档吗？此操作不可撤销！", () =>
        {
            TT.ClearAllSaving();
            #if UNITY_EDITOR || DEVELOPMENT_BUILD
            Debug.Log("全部存档已清空");
            #endif
        });
    }

    private void ShowConfirmDialog(string message, System.Action onConfirm)
    {
        // 展示确认弹窗，用户确认后才执行 onConfirm
    }

    /// <summary>
    /// 获取缓存占用大小
    /// </summary>
    public string GetCacheSizeInfo()
    {
        long bytes = TT.GetSavingDiskSize();
        if (bytes < 1024)
            return $"{bytes} B";
        else if (bytes < 1024 * 1024)
            return $"{bytes / 1024f:F1} KB";
        else
            return $"{bytes / (1024f * 1024f):F1} MB";
    }
}

[System.Serializable]
public class PlayerProfile
{
    public string playerName;
    public int level;
    public int coins;
    public long playTimeSeconds;
}

[System.Serializable]
public class GameSettings
{
    public float musicVolume = 0.8f;
    public float sfxVolume = 1.0f;
    public bool vibrationEnabled = true;
    public int qualityLevel = 1;
}
```

---

## 二、PlayerPrefs

Unity 原生 `PlayerPrefs` 在 WebGL / 小游戏容器环境中不可用。抖音小游戏 Unity SDK 提供了 `TT.PlayerPrefs` 作为完全兼容的替代方案，接口与 Unity 原生 `PlayerPrefs` 一致，底层映射到宿主 App 提供的键值存储系统。

### 2.1 SetInt / GetInt

**说明**: 存储和读取整数类型数据。

**语法**:

```csharp
public static void SetInt(string key, int value)
public static int GetInt(string key, int defaultValue = 0)
```

**参数说明**:

| 参数 | 类型 | 必填 | 默认值 | 说明 |
|------|------|------|--------|------|
| key | string | 是 | - | 存储键名 |
| value | int | 是 | - | 要存储的整数值 |
| defaultValue | int | 否 | 0 | 键不存在时返回的默认值 |

---

### 2.2 SetFloat / GetFloat

**说明**: 存储和读取浮点数类型数据。

**语法**:

```csharp
public static void SetFloat(string key, float value)
public static float GetFloat(string key, float defaultValue = 0f)
```

**参数说明**:

| 参数 | 类型 | 必填 | 默认值 | 说明 |
|------|------|------|--------|------|
| key | string | 是 | - | 存储键名 |
| value | float | 是 | - | 要存储的浮点数值 |
| defaultValue | float | 否 | 0f | 键不存在时返回的默认值 |

---

### 2.3 SetString / GetString

**说明**: 存储和读取字符串类型数据。

**语法**:

```csharp
public static void SetString(string key, string value)
public static string GetString(string key, string defaultValue = "")
```

**参数说明**:

| 参数 | 类型 | 必填 | 默认值 | 说明 |
|------|------|------|--------|------|
| key | string | 是 | - | 存储键名 |
| value | string | 是 | - | 要存储的字符串值 |
| defaultValue | string | 否 | "" | 键不存在时返回的默认值 |

---

### 2.4 HasKey

**说明**: 判断指定 key 是否存在。

**语法**:

```csharp
public static bool HasKey(string key)
```

**参数说明**:

| 参数 | 类型 | 必填 | 默认值 | 说明 |
|------|------|------|--------|------|
| key | string | 是 | - | 要检查的键名 |

**返回值**: `bool`，`true` 表示该键存在。

---

### 2.5 DeleteKey

**说明**: 删除指定 key 的数据。

**语法**:

```csharp
public static void DeleteKey(string key)
```

**参数说明**:

| 参数 | 类型 | 必填 | 默认值 | 说明 |
|------|------|------|--------|------|
| key | string | 是 | - | 要删除的键名 |

---

### 2.6 DeleteAll

**说明**: 删除所有 PlayerPrefs 数据。不可逆操作，调用前应提示用户。

**语法**:

```csharp
public static void DeleteAll()
```

---

### 2.7 Save

**说明**: 将修改写入磁盘。Unity 原生 PlayerPrefs 默认在游戏退出时自动保存，但在 WebGL 环境下需显式调用 `Save()` 以确保数据落盘。抖音小游戏环境中同样建议在关键数据修改后手动调用此方法。

**语法**:

```csharp
public static void Save()
```

---

### 2.8 代码示例

```csharp
using UnityEngine;
using TT;

/// <summary>
/// PlayerPrefs 完整使用示例: 游戏设置管理
/// </summary>
public class GameSettingsManager : MonoBehaviour
{
    private const string KEY_MUSIC_VOLUME = "MusicVolume";
    private const string KEY_SFX_VOLUME = "SfxVolume";
    private const string KEY_HIGH_SCORE = "HighScore";
    private const string KEY_PLAYER_NAME = "PlayerName";
    private const string KEY_FIRST_RUN = "FirstRun";

    void Start()
    {
        // 检查是否首次运行
        if (!TT.PlayerPrefs.HasKey(KEY_FIRST_RUN))
        {
            InitDefaultSettings();
            TT.PlayerPrefs.SetInt(KEY_FIRST_RUN, 1);
            TT.PlayerPrefs.Save();
            Debug.Log("首次运行，已初始化默认设置");
        }
        else
        {
            LoadSettings();
        }
    }

    /// <summary>
    /// 初始化默认设置
    /// </summary>
    private void InitDefaultSettings()
    {
        TT.PlayerPrefs.SetFloat(KEY_MUSIC_VOLUME, 0.8f);
        TT.PlayerPrefs.SetFloat(KEY_SFX_VOLUME, 1.0f);
        TT.PlayerPrefs.SetInt(KEY_HIGH_SCORE, 0);
        TT.PlayerPrefs.SetString(KEY_PLAYER_NAME, "新玩家");
    }

    /// <summary>
    /// 加载所有设置
    /// </summary>
    private void LoadSettings()
    {
        float musicVolume = TT.PlayerPrefs.GetFloat(KEY_MUSIC_VOLUME, 0.8f);
        float sfxVolume = TT.PlayerPrefs.GetFloat(KEY_SFX_VOLUME, 1.0f);
        int highScore = TT.PlayerPrefs.GetInt(KEY_HIGH_SCORE, 0);
        string playerName = TT.PlayerPrefs.GetString(KEY_PLAYER_NAME, "新玩家");

        // ⚠️ 安全：玩家名称为个人信息，生产环境禁止打印
        #if UNITY_EDITOR || DEVELOPMENT_BUILD
        Debug.Log($"设置加载完成: 音乐={musicVolume}, 音效={sfxVolume}, " +
                  $"最高分={highScore}, 玩家名={playerName}");
        #else
        Debug.Log($"设置加载完成: 音乐={musicVolume}, 音效={sfxVolume}, 最高分={highScore}");
        #endif

        ApplySettings(musicVolume, sfxVolume);
    }

    /// <summary>
    /// 更新并持久化最高分
    /// </summary>
    public void UpdateHighScore(int newScore)
    {
        int currentHigh = TT.PlayerPrefs.GetInt(KEY_HIGH_SCORE, 0);
        if (newScore > currentHigh)
        {
            TT.PlayerPrefs.SetInt(KEY_HIGH_SCORE, newScore);
            TT.PlayerPrefs.Save();
            Debug.Log($"刷新最高分: {newScore}");
        }
    }

    /// <summary>
    /// 更新音乐音量
    /// </summary>
    public void SetMusicVolume(float volume)
    {
        volume = Mathf.Clamp01(volume);
        TT.PlayerPrefs.SetFloat(KEY_MUSIC_VOLUME, volume);
        TT.PlayerPrefs.Save();
    }

    /// <summary>
    /// 重置所有设置（⚠️ 不可逆，必须用户确认后执行）
    /// </summary>
    public void ResetAllSettings()
    {
        // ⚠️ 安全：DeleteAll 不可逆，调用前必须弹窗获得用户明确确认
        ShowConfirmDialog("确定要重置所有设置吗？此操作不可撤销！", () =>
        {
            TT.PlayerPrefs.DeleteAll();
            #if UNITY_EDITOR || DEVELOPMENT_BUILD
            Debug.Log("所有设置已重置");
            #endif
        });
    }

    private void ApplySettings(float musicVol, float sfxVol)
    {
        // 应用到音频系统
        AudioListener.volume = musicVol;
    }
}
```

---

## 三、文件系统

抖音小游戏提供了完整的文件系统 API，支持文件的读写、目录管理、文件信息查询等操作。文件系统操作分为**同步**（方法名以 `Sync` 结尾）和**异步**两种模式。同步方法建议在主线程中限制使用，大文件操作推荐用异步方法。

### 3.1 TT.GetFileSystemManager

**说明**: 获取全局唯一的文件系统管理器实例。所有文件操作均通过此实例进行。

**语法**:

```csharp
public static TTFileSystemManager GetFileSystemManager()
```

**返回值**: `TTFileSystemManager`，全局单例文件管理器。

**代码示例**:

```csharp
TTFileSystemManager fs = TT.GetFileSystemManager();
```

---

### 3.2 Access / AccessSync

**说明**: 检查文件或目录是否存在。异步版本通过回调返回结果，同步版本直接返回 `bool`。

**语法**:

```csharp
// 异步
public void Access(string path, Action<bool> callback)

// 同步
public bool AccessSync(string path)
```

**参数说明**:

| 参数 | 类型 | 必填 | 默认值 | 说明 |
|------|------|------|--------|------|
| path | string | 是 | - | 要检查的文件或目录路径 |
| callback | Action\<bool\> | 是 | - | 异步回调，`true` 表示存在 |

---

### 3.3 CopyFile / CopyFileSync

**说明**: 复制文件。源路径和目标路径的父目录必须已存在。

**语法**:

```csharp
// 异步
public void CopyFile(string srcPath, string destPath, Action<bool> callback = null)

// 同步
public bool CopyFileSync(string srcPath, string destPath)
```

**参数说明**:

| 参数 | 类型 | 必填 | 默认值 | 说明 |
|------|------|------|--------|------|
| srcPath | string | 是 | - | 源文件路径 |
| destPath | string | 是 | - | 目标文件路径 |
| callback | Action\<bool\> | 否 | null | 异步回调，`true` 表示复制成功 |

---

### 3.4 Mkdir / MkdirSync

**说明**: 创建目录。

**语法**:

```csharp
// 异步
public void Mkdir(string dirPath, bool recursive = false, Action<bool> callback = null)

// 同步
public bool MkdirSync(string dirPath, bool recursive = false)
```

**参数说明**:

| 参数 | 类型 | 必填 | 默认值 | 说明 |
|------|------|------|--------|------|
| dirPath | string | 是 | - | 要创建的目录路径 |
| recursive | bool | 否 | false | 是否递归创建父级目录。`true` 时自动创建路径中所有不存在的父目录 |
| callback | Action\<bool\> | 否 | null | 异步回调，`true` 表示创建成功 |

---

### 3.5 Readdir / ReaddirSync

**说明**: 读取目录内容，返回目录下的文件列表。

**语法**:

```csharp
// 异步
public void Readdir(string dirPath, Action<string[]> callback)

// 同步
public string[] ReaddirSync(string dirPath)
```

**参数说明**:

| 参数 | 类型 | 必填 | 默认值 | 说明 |
|------|------|------|--------|------|
| dirPath | string | 是 | - | 目录路径 |
| callback | Action\<string[]\> | 是 | - | 异步回调，参数为文件名数组 |

---

### 3.6 ReadFile / ReadFileSync

**说明**: 读取文件内容。支持 utf8、base64、binary 三种编码格式。

**语法**:

```csharp
// 异步
public void ReadFile(string filePath, string encoding, Action<string> callback)

// 同步
public string ReadFileSync(string filePath, string encoding = "utf8")
```

**参数说明**:

| 参数 | 类型 | 必填 | 默认值 | 说明 |
|------|------|------|--------|------|
| filePath | string | 是 | - | 文件路径 |
| encoding | string | 是 | "utf8" | 编码格式: `"utf8"`、`"base64"`、`"binary"` |
| callback | Action\<string\> | 是 | - | 异步回调，参数为文件内容字符串 |

---

### 3.7 WriteFile / WriteFileSync

**说明**: 写入文件内容（覆盖模式）。若文件不存在则创建，存在则覆盖原内容。

**语法**:

```csharp
// 异步
public void WriteFile(string filePath, string data, string encoding, Action<bool> callback = null)

// 同步
public bool WriteFileSync(string filePath, string data, string encoding = "utf8")
```

**参数说明**:

| 参数 | 类型 | 必填 | 默认值 | 说明 |
|------|------|------|--------|------|
| filePath | string | 是 | - | 文件路径 |
| data | string | 是 | - | 要写入的数据 |
| encoding | string | 是 | "utf8" | 编码格式: `"utf8"`、`"base64"`、`"binary"` |
| callback | Action\<bool\> | 否 | null | 异步回调，`true` 表示写入成功 |

---

### 3.8 AppendFile / AppendFileSync

**说明**: 向文件追加内容。若文件不存在则创建。

**语法**:

```csharp
// 异步
public void AppendFile(string filePath, string data, string encoding, Action<bool> callback = null)

// 同步
public bool AppendFileSync(string filePath, string data, string encoding = "utf8")
```

**参数说明**:

| 参数 | 类型 | 必填 | 默认值 | 说明 |
|------|------|------|--------|------|
| filePath | string | 是 | - | 文件路径 |
| data | string | 是 | - | 要追加的内容 |
| encoding | string | 是 | "utf8" | 编码格式 |
| callback | Action\<bool\> | 否 | null | 异步回调，`true` 表示追加成功 |

---

### 3.9 Rename / RenameSync

**说明**: 重命名文件或目录。

**语法**:

```csharp
// 异步
public void Rename(string oldPath, string newPath, Action<bool> callback = null)

// 同步
public bool RenameSync(string oldPath, string newPath)
```

**参数说明**:

| 参数 | 类型 | 必填 | 默认值 | 说明 |
|------|------|------|--------|------|
| oldPath | string | 是 | - | 原始路径 |
| newPath | string | 是 | - | 新路径 |
| callback | Action\<bool\> | 否 | null | 异步回调，`true` 表示重命名成功 |

---

### 3.10 Rmdir / RmdirSync

**说明**: 删除目录。

**语法**:

```csharp
// 异步
public void Rmdir(string dirPath, bool recursive = false, Action<bool> callback = null)

// 同步
public bool RmdirSync(string dirPath, bool recursive = false)
```

**参数说明**:

| 参数 | 类型 | 必填 | 默认值 | 说明 |
|------|------|------|--------|------|
| dirPath | string | 是 | - | 要删除的目录路径 |
| recursive | bool | 否 | false | 是否递归删除。`false` 时目录非空会删除失败 |
| callback | Action\<bool\> | 否 | null | 异步回调，`true` 表示删除成功 |

---

### 3.11 Unlink / UnlinkSync

**说明**: 删除单个文件。

**语法**:

```csharp
// 异步
public void Unlink(string filePath, Action<bool> callback = null)

// 同步
public bool UnlinkSync(string filePath)
```

**参数说明**:

| 参数 | 类型 | 必填 | 默认值 | 说明 |
|------|------|------|--------|------|
| filePath | string | 是 | - | 要删除的文件路径 |
| callback | Action\<bool\> | 否 | null | 异步回调，`true` 表示删除成功 |

---

### 3.12 Stat / StatSync

**说明**: 获取文件或目录的详细信息。

**语法**:

```csharp
// 异步
public void Stat(string path, bool recursive = false, Action<Stats> callback = null)

// 同步
public Stats StatSync(string path, bool recursive = false)
```

**参数说明**:

| 参数 | 类型 | 必填 | 默认值 | 说明 |
|------|------|------|--------|------|
| path | string | 是 | - | 文件或目录路径 |
| recursive | bool | 否 | false | 是否递归获取子目录信息 |
| callback | Action\<Stats\> | 否 | null | 异步回调，参数为 Stats 对象 |

**Stats 对象说明**:

| 属性/方法 | 类型 | 说明 |
|-----------|------|------|
| size | long | 文件大小（字节） |
| isFile() | bool | 是否为文件 |
| isDirectory() | bool | 是否为目录 |
| lastModifiedTime | long | 最后修改时间戳 |

---

### 3.13 Open / OpenSync

**说明**: 打开文件并返回文件描述符（fd）。后续可对 fd 进行读写、截断等操作。操作完成后必须调用 `Close` 释放资源。

**语法**:

```csharp
// 异步
public void Open(string filePath, string flag, Action<int> callback)

// 同步
public int OpenSync(string filePath, string flag)
```

**参数说明**:

| 参数 | 类型 | 必填 | 默认值 | 说明 |
|------|------|------|--------|------|
| filePath | string | 是 | - | 文件路径 |
| flag | string | 是 | - | 打开模式: `"r"` 只读、`"w"` 只写（覆盖）、`"a"` 追加写 |

**返回值**: `int`，文件描述符。失败时返回负值。

---

### 3.14 Close / CloseSync

**说明**: 关闭文件描述符，释放文件句柄资源。

**语法**:

```csharp
// 异步
public void Close(int fd, Action<bool> callback = null)

// 同步
public bool CloseSync(int fd)
```

---

### 3.15 Write / WriteSync（fd 模式）

**说明**: 向已打开的文件描述符写入数据。

**语法**:

```csharp
// 异步
public void Write(int fd, string data, string encoding, Action<bool> callback = null)

// 同步
public bool WriteSync(int fd, string data, string encoding = "utf8")
```

---

### 3.16 Read / ReadSync（fd 模式）

**说明**: 从文件描述符读取数据。

**语法**:

```csharp
// 异步
public void Read(int fd, string encoding, Action<string> callback)

// 同步
public string ReadSync(int fd, string encoding = "utf8")
```

---

### 3.17 Fstat / FstatSync

**说明**: 获取文件描述符对应文件的信息。

**语法**:

```csharp
// 异步
public void Fstat(int fd, Action<Stats> callback)

// 同步
public Stats FstatSync(int fd)
```

---

### 3.18 Ftruncate / FtruncateSync

**说明**: 对文件描述符执行截断操作。

**语法**:

```csharp
// 异步
public void Ftruncate(int fd, long length, Action<bool> callback = null)

// 同步
public bool FtruncateSync(int fd, long length)
```

**参数说明**:

| 参数 | 类型 | 必填 | 默认值 | 说明 |
|------|------|------|--------|------|
| fd | int | 是 | - | 文件描述符 |
| length | long | 是 | - | 截断后文件长度（字节） |

---

### 3.19 Truncate / TruncateSync

**说明**: 对文件路径执行截断操作。

**语法**:

```csharp
// 异步
public void Truncate(string filePath, long length, Action<bool> callback = null)

// 同步
public bool TruncateSync(string filePath, long length)
```

---

### 3.20 ReadDir / ReadDirSync

**说明**: 读取目录内容（与 Readdir 类似的另一个版本）。

**语法**:

```csharp
// 异步
public void ReadDir(string dirPath, Action<string[]> callback)

// 同步
public string[] ReadDirSync(string dirPath)
```

---

### 3.21 异步特有方法

以下方法仅有异步版本，无对应的 Sync 同步版本。

**ReadCompressedFile**: 读取压缩文件内容。

```csharp
public void ReadCompressedFile(string filePath, string compressionType, Action<string> callback)
```

**GetSavedFileList**: 获取已保存的文件列表。

```csharp
public void GetSavedFileList(Action<SavedFileInfo[]> callback)
```

**GetFileInfo**: 获取文件详细信息。

```csharp
public void GetFileInfo(string filePath, Action<FileInfo> callback)
```

---

### 3.22 文件读写完整代码示例

```csharp
using UnityEngine;
using TT;

/// <summary>
/// 文件系统管理器: 存档文件的完整读写流程
/// </summary>
public class FileSystemSaveManager : MonoBehaviour
{
    private TTFileSystemManager m_Fs;
    private string m_DataDir;

    void Start()
    {
        if (TT.InContainerEnv)
        {
            m_Fs = TT.GetFileSystemManager();
            // 用户数据目录通过环境变量获取
            m_DataDir = GetUserDataPath();
            InitDirectory();
        }
    }

    /// <summary>
    /// 获取用户可读写的目录路径
    /// </summary>
    private string GetUserDataPath()
    {
        // 用户数据目录路径，此处通过 Unity 持久化路径拼接
        string path = Application.persistentDataPath + "/game_data";
        return path;
    }

    /// <summary>
    /// 初始化目录结构
    /// </summary>
    private void InitDirectory()
    {
        if (m_Fs == null) return;

        // 创建必要的子目录（递归创建，忽略已存在的情况）
        m_Fs.MkdirSync(m_DataDir, true);
        m_Fs.MkdirSync(m_DataDir + "/saves", true);
        m_Fs.MkdirSync(m_DataDir + "/config", true);
        m_Fs.MkdirSync(m_DataDir + "/logs", true);

        Debug.Log($"数据目录初始化完成: {m_DataDir}");
    }

    /// <summary>
    /// 保存游戏存档（JSON 文件）
    /// </summary>
    public void SaveGameData(string slotName, GameSaveData data)
    {
        if (m_Fs == null) return;

        string json = JsonUtility.ToJson(data);
        string filePath = $"{m_DataDir}/saves/{slotName}.json";

        // 异步写入，避免主线程卡顿
        m_Fs.WriteFile(filePath, json, "utf8", (success) =>
        {
            if (success)
            {
                Debug.Log($"存档 {slotName} 已保存: {filePath}");
            }
            else
            {
                Debug.LogError($"存档 {slotName} 保存失败");
            }
        });
    }

    /// <summary>
    /// 加载游戏存档
    /// </summary>
    public void LoadGameData(string slotName, System.Action<GameSaveData> onLoaded)
    {
        if (m_Fs == null)
        {
            onLoaded?.Invoke(null);
            return;
        }

        string filePath = $"{m_DataDir}/saves/{slotName}.json";

        // 先检查文件是否存在
        if (!m_Fs.AccessSync(filePath))
        {
            Debug.LogWarning($"存档 {slotName} 不存在");
            onLoaded?.Invoke(null);
            return;
        }

        m_Fs.ReadFile(filePath, "utf8", (content) =>
        {
            try
            {
                GameSaveData data = JsonUtility.FromJson<GameSaveData>(content);
                Debug.Log($"存档 {slotName} 已加载");
                onLoaded?.Invoke(data);
            }
            catch (System.Exception e)
            {
                Debug.LogError($"存档解析失败: {e.Message}");
                onLoaded?.Invoke(null);
            }
        });
    }

    /// <summary>
    /// 获取所有存档列表
    /// </summary>
    public string[] GetSaveSlots()
    {
        if (m_Fs == null) return new string[0];

        string savesPath = $"{m_DataDir}/saves";
        if (!m_Fs.AccessSync(savesPath)) return new string[0];

        string[] files = m_Fs.ReaddirSync(savesPath);
        return files;
    }

    /// <summary>
    /// 删除指定存档
    /// </summary>
    public void DeleteSaveSlot(string slotName)
    {
        if (m_Fs == null) return;

        string filePath = $"{m_DataDir}/saves/{slotName}.json";
        m_Fs.Unlink(filePath, (success) =>
        {
            Debug.Log(success ? $"存档 {slotName} 已删除" : $"存档 {slotName} 删除失败");
        });
    }

    /// <summary>
    /// 追加日志（使用文件描述符模式，性能更高）
    /// </summary>
    public void AppendLog(string message)
    {
        if (m_Fs == null) return;

        string logPath = $"{m_DataDir}/logs/game.log";
        string logLine = $"[{System.DateTime.Now:yyyy-MM-dd HH:mm:ss}] {message}\n";

        // 使用 Append 方式追加，效率高于读写整个文件
        m_Fs.AppendFile(logPath, logLine, "utf8");
    }

    /// <summary>
    /// 获取存档文件大小信息
    /// </summary>
    public string GetSaveFileInfo(string slotName)
    {
        if (m_Fs == null) return "未知";

        string filePath = $"{m_DataDir}/saves/{slotName}.json";
        if (!m_Fs.AccessSync(filePath)) return "不存在";

        var stat = m_Fs.StatSync(filePath);
        return $"大小: {stat.size} 字节, 修改时间: {stat.lastModifiedTime}";
    }

    /// <summary>
    /// 清理所有数据（⚠️ 极度危险：递归删除全部文件，不可逆，必须用户确认后执行）
    /// </summary>
    public void ClearAllData()
    {
        // ⚠️ 安全：递归删除全部数据不可逆，调用前必须弹窗获得用户明确确认
        ShowConfirmDialog("确定要清理所有数据吗？此操作将删除全部存档、配置和日志，不可撤销！", () =>
        {
            if (m_Fs == null) return;

            if (m_Fs.AccessSync(m_DataDir))
            {
                m_Fs.RmdirSync(m_DataDir, true);
            }
            InitDirectory();
            #if UNITY_EDITOR || DEVELOPMENT_BUILD
            Debug.Log("全部数据已清理并重新初始化");
            #endif
        });
    }
}

[System.Serializable]
public class GameSaveData
{
    public string saveTime;
    public int level;
    public int score;
    public int coins;
    public float playTime;
}
```

---

## 四、用户数据目录

### 4.1 可读写路径

用户数据目录是小游戏唯一的可自由读写区域。其他路径（如代码包内文件）均为只读。

```csharp
// 方式一: 通过环境变量获取（推荐）
string userPath = TTEnv.UserDataPath;

// 方式二: 通过 Application.persistentDataPath
string persistentPath = Application.persistentDataPath;
```

### 4.2 路径规范

| 路径类型 | 前缀 | 权限 | 说明 |
|----------|------|------|------|
| 用户数据目录 | `ttfile://` 或系统路径 | 读写 | 持久化数据存储区域，唯一的可读写位置 |
| 代码包内文件 | `/` | 只读 | 随代码包分发的资源文件 |
| 临时目录 | 系统临时路径 | 读写 | 临时文件，可能被系统回收 |

```csharp
// 路径使用规范示例
public class PathHelper
{
    private string m_UserDataPath;

    public PathHelper()
    {
        m_UserDataPath = TTEnv.UserDataPath;
    }

    // 获取存档目录
    public string GetSavePath()
    {
        return $"{m_UserDataPath}/saves";
    }

    // 获取配置文件路径
    public string GetConfigPath(string configName)
    {
        return $"{m_UserDataPath}/config/{configName}.json";
    }

    // 获取日志目录
    public string GetLogPath()
    {
        return $"{m_UserDataPath}/logs";
    }

    // 构建用户数据下的完整路径
    public string BuildPath(params string[] segments)
    {
        return string.Join("/", segments);
    }
}
```

---

## 五、存储最佳实践

### 5.1 存储方案选型

| 场景 | 推荐方案 | 原因 |
|------|---------|------|
| 少量设置项（音量、开关、玩家名） | `TT.PlayerPrefs` | 接口简单，与 Unity 原生一致，自动管理 |
| 存档数据（关卡进度、道具列表） | 数据缓存 + JSON（`TT.Save`/`TT.LoadSaving`） | 键值对存储，支持对象序列化，上限约 10MB |
| 大型存档、日志文件 | 文件系统（`TTFileSystemManager`） | 支持目录管理、追加写入、文件描述符操作 |
| 临时数据 | 文件系统临时目录 | 无需持久化，系统自动回收 |

### 5.2 同步 vs 异步方法选择

| 场景 | 推荐 | 说明 |
|------|------|------|
| 启动初始化、目录检查 | 同步（Sync） | 必须在游戏逻辑启动前完成 |
| 读存档（小文件 <100KB） | 同步（Sync） | 加载时间可忽略，简化逻辑 |
| 写存档（大文件 >100KB） | 异步 | 避免主线程卡顿 |
| 日志追加 | 异步 | 不影响游戏帧率 |
| 文件列表/状态检查 | 同步（Sync） | 数据量小，即时返回 |

### 5.3 序列化方式

```csharp
// JSON 序列化: 推荐用于存档数据（可读性好、跨版本兼容）
string json = JsonUtility.ToJson(saveData);
TT.Save("save_slot_1", json);

// 读取加防御: 处理版本升级导致的字段缺失
var data = JsonUtility.FromJson<GameSaveData>(TT.LoadSaving("save_slot_1"));
if (data == null) data = GetDefaultSaveData();

// 二进制序列化: 适用于大型二进制数据（截图、序列化后的 AssetBundle）
byte[] bytes = ProtoBufSerialize(saveData);   // 或使用 BinaryFormatter
string base64 = System.Convert.ToBase64String(bytes);
m_Fs.WriteFileSync(savePath, base64, "base64");
```

### 5.4 路径规范

```csharp
// 使用 Path.Combine 构建路径，避免硬编码分隔符
string savePath = System.IO.Path.Combine(m_UserDataPath, "saves", "slot_1.json");

// 不要使用绝对路径，始终基于用户数据目录
// 错误: "/Users/xxx/save.json"
// 正确: TTEnv.UserDataPath + "/saves/slot_1.json"

// 目录操作前确保父目录存在
string dir = System.IO.Path.GetDirectoryName(filePath);
if (!m_Fs.AccessSync(dir))
{
    m_Fs.MkdirSync(dir, true);
}
```

### 5.5 错误处理

```csharp
/// <summary>
/// 安全的文件读取，包含完整的错误处理和降级逻辑
/// </summary>
public static T SafeReadJson<T>(TTFileSystemManager fs, string filePath, T defaultValue) where T : class
{
    try
    {
        // 检查文件是否存在
        if (fs == null || !fs.AccessSync(filePath))
        {
            Debug.LogWarning($"文件不存在: {filePath}，使用默认值");
            return defaultValue;
        }

        string content = fs.ReadFileSync(filePath, "utf8");
        if (string.IsNullOrEmpty(content))
        {
            Debug.LogWarning($"文件为空: {filePath}");
            return defaultValue;
        }

        return JsonUtility.FromJson<T>(content) ?? defaultValue;
    }
    catch (System.Exception e)
    {
        Debug.LogError($"文件读取失败 [{filePath}]: {e.Message}");
        return defaultValue;
    }
}
```

### 5.6 存储限制

| 限制项 | 上限 | 说明 |
|--------|------|------|
| 数据缓存总大小 | 约 10MB | 所有 `TT.Save` 数据的总和 |
| 单 key 数据大小 | 建议不超过 1MB | 过大数据建议使用文件系统 |
| PlayerPrefs 总大小 | 约 10MB | 与数据缓存共享配额 |
| 用户数据目录总大小 | 约 200MB | 依赖宿主 App 分配，可能动态变化 |
| 文件路径最大长度 | 1024 字符 | 超过可能导致操作失败 |

### 5.7 完整存储架构示例

```csharp
using UnityEngine;
using TT;

/// <summary>
/// 统一存储层: 根据需要自动选择最合适的存储方案
/// </summary>
public class UnifiedStorageManager : MonoBehaviour
{
    private TTFileSystemManager m_Fs;
    private string m_UserDataPath;

    void Awake()
    {
        m_UserDataPath = TTEnv.UserDataPath;
        m_Fs = TT.GetFileSystemManager();

        // 确保目录结构存在
        EnsureDirectoryExists(m_UserDataPath + "/saves");
        EnsureDirectoryExists(m_UserDataPath + "/config");
    }

    /// <summary>
    /// 小而频繁的数据: 使用 PlayerPrefs
    /// </summary>
    public void SaveSmallSetting(string key, string value)
    {
        TT.PlayerPrefs.SetString(key, value);
        TT.PlayerPrefs.Save();
    }

    /// <summary>
    /// 中等大小的对象数据: 使用数据缓存
    /// </summary>
    public void SaveObjectData<T>(string key, T data)
    {
        string json = JsonUtility.ToJson(data);
        TT.Save(key, json);
    }

    public T LoadObjectData<T>(string key, T defaultValue = default)
    {
        string json = TT.LoadSaving(key);
        if (string.IsNullOrEmpty(json)) return defaultValue;
        try
        {
            return JsonUtility.FromJson<T>(json);
        }
        catch
        {
            return defaultValue;
        }
    }

    /// <summary>
    /// 大文件或日志: 使用文件系统
    /// </summary>
    public void SaveLargeFile(string relativePath, string content)
    {
        string fullPath = m_UserDataPath + "/" + relativePath;
        EnsureDirectoryExists(System.IO.Path.GetDirectoryName(fullPath));
        m_Fs.WriteFile(fullPath, content, "utf8", (success) =>
        {
            Debug.Log(success ? $"文件已保存: {fullPath}" : $"文件保存失败: {fullPath}");
        });
    }

    private void EnsureDirectoryExists(string dirPath)
    {
        if (!m_Fs.AccessSync(dirPath))
        {
            m_Fs.MkdirSync(dirPath, true);
        }
    }
}
```
