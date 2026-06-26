# ffmpeg 安装说明

## 系统环境

本机 pip install 需要 root 权限，无法通过 apt 安装。

## 方案一：imageio-ffmpeg（已采用）

```bash
pip install imageio-ffmpeg
```

路径：`/usr/local/lib/python3.10/dist-packages/imageio_ffmpeg/binaries/ffmpeg-linux-x86_64-v7.0.2`

使用方式（直接调用完整路径）：
```bash
FFMPEG=/usr/local/lib/python3.10/dist-packages/imageio_ffmpeg/binaries/ffmpeg-linux-x86_64-v7.0.2
$FFMPEG [args]
```

## 方案二：conda

```bash
conda install -c conda-forge ffmpeg
```

## 方案三：静态二进制（推荐生产环境）

```bash
# 下载静态编译的 ffmpeg
wget https://johnvansickle.com/ffmpeg/releases/ffmpeg-release-amd64-static.tar.xz
tar -xf ffmpeg-release-amd64-static.tar.xz
mv ffmpeg-*-amd64-static/ffmpeg /usr/local/bin/
```

## 验证安装

```bash
ffmpeg -version
# 或
python3 -c "import imageio_ffmpeg; print(imageio_ffmpeg.get_ffmpeg_exe())"
```
