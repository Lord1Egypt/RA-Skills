# 文件类型速查表

## 文档类

| 扩展名 | 类型 | 默认归宿 |
|--------|------|----------|
| `.md` | Markdown 文档 | references/ |
| `.docx` | Word 文档 | references/ |
| `.doc` | Word 文档 (旧) | references/ |
| `.pdf` | PDF 文档 | references/ |
| `.txt` | 纯文本 | references/ |
| `.xlsx` | Excel 表格 | references/ |
| `.xls` | Excel 表格 (旧) | references/ |
| `.csv` | CSV 数据 | references/ |
| `.pptx` | PPT 演示 | references/ |
| `.ppt` | PPT 演示 (旧) | references/ |

## 代码类

| 扩展名 | 类型 | 默认归宿 |
|--------|------|----------|
| `.py` | Python | projects/ |
| `.js` | JavaScript | projects/ |
| `.ts` | TypeScript | projects/ |
| `.cs` | C# / C Sharp | projects/ |
| `.cpp` | C++ | projects/ |
| `.c` | C | projects/ |
| `.java` | Java | projects/ |
| `.go` | Go | projects/ |
| `.rs` | Rust | projects/ |
| `.rb` | Ruby | projects/ |
| `.php` | PHP | projects/ |
| `.swift` | Swift | projects/ |
| `.kt` | Kotlin | projects/ |
| `.html` | HTML | projects/ |
| `.css` | CSS | projects/ |
| `.scss` | SCSS | projects/ |
| `.vue` | Vue 组件 | projects/ |
| `.jsx` | React 组件 | projects/ |
| `.tsx` | React TSX | projects/ |
| `.sh` | Shell 脚本 | projects/ |
| `.ps1` | PowerShell | projects/ |
| `.bat` | Batch 脚本 | projects/ |
| `.sql` | SQL | projects/ |
| `.xml` | XML | projects/ |
| `.yaml` / `.yml` | YAML 配置 | projects/ |
| `.json` | JSON | projects/ |
| `.toml` | TOML | projects/ |

## 游戏/Unity 专项

| 扩展名 | 类型 | 默认归宿 |
|--------|------|----------|
| `.unity` | Unity 场景 | projects/ |
| `.prefab` | Unity 预制体 | projects/ |
| `.mat` | Unity 材质 | projects/ |
| `.asset` | Unity 资源 | projects/ |
| `.shader` | Shader 代码 | projects/ |
| `.compute` | Compute Shader | projects/ |
| `.asmdef` | Unity 程序集定义 | projects/ |
| `.controller` | 动画控制器 | projects/ |
| `.anim` | 动画片段 | projects/ |
| `.physicMaterial` | 物理材质 | projects/ |
| `.inputactions` | 输入配置 | projects/ |

## 素材类

| 扩展名 | 类型 | 默认归宿 |
|--------|------|----------|
| `.png` | PNG 图片 | projects/ 或 scratch/ |
| `.jpg` / `.jpeg` | JPG 图片 | projects/ 或 scratch/ |
| `.gif` | GIF 动图 | projects/ 或 scratch/ |
| `.webp` | WebP 图片 | projects/ 或 scratch/ |
| `.svg` | SVG 矢量图 | projects/ |
| `.psd` | Photoshop 源文件 | projects/ |
| `.ai` | Illustrator 源文件 | projects/ |
| `.blend` | Blender 源文件 | projects/ |
| `.fbx` | FBX 模型 | projects/ |
| `.obj` | OBJ 模型 | projects/ |
| `.mp3` | MP3 音频 | projects/ |
| `.wav` | WAV 音频 | projects/ |
| `.ogg` | OGG 音频 | projects/ |
| `.mp4` | MP4 视频 | projects/ |
| `.mov` | MOV 视频 | projects/ |
| `.webm` | WebM 视频 | projects/ |
| `.ttf` | 字体文件 | references/ |
| `.otf` | 字体文件 | references/ |

## 模型/AI 专项

| 扩展名 | 类型 | 默认归宿 |
|--------|------|----------|
| `.h5` | Keras 模型 | projects/ |
| `.pt` / `.pth` | PyTorch 模型 | projects/ |
| `.ckpt` | TensorFlow 检查点 | projects/ |
| `.pkl` / `.pickle` | Pickle 数据 | projects/ |
| `.onnx` | ONNX 模型 | projects/ |
| `.safetensors` | SafeTensor | projects/ |
| `.npy` | NumPy 数组 | projects/ |
| `.npz` | NumPy 压缩包 | projects/ |
| `.parquet` | Parquet 数据 | projects/ |

## 临时/备份类

| 扩展名 | 类型 | 默认归宿 | 处理方式 |
|--------|------|----------|----------|
| `*_temp*` | 临时文件 | scratch/ | 30天后归档 |
| `*~` | 临时文件 | scratch/ | 30天后归档 |
| `*.tmp` | 临时文件 | scratch/ | 30天后归档 |
| `*.bak` | 备份文件 | scratch/ | 30天后归档 |
| `*.cache` | 缓存文件 | scratch/ | 30天后归档 |
| `*.log` | 日志文件 | scratch/ | 7天后归档 |

## 压缩/归档类

| 扩展名 | 类型 | 建议归宿 |
|--------|------|----------|
| `.zip` | ZIP 压缩包 | archives/ 或 解压后分流 |
| `.rar` | RAR 压缩包 | archives/ 或 解压后分流 |
| `.7z` | 7Z 压缩包 | archives/ 或 解压后分流 |
| `.tar` | TAR 归档 | archives/ 或 解压后分流 |
| `.gz` | GZ 压缩 | archives/ |

## 版本标记文件（识别用）

- `*_v1*`, `*_v2*`, `*_v3*` - 版本号
- `*_draft*` - 草稿版
- `*_final*` - 最终版
- `*_old*` / `*_new*` - 新旧版本
- `*_backup*` - 备份
- `*_copy*` / `*_副本*` - 副本
- `*_01*`, `*_02*` - 序号
