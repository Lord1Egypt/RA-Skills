#!/usr/bin/env python3
"""
B 站视频转录专家 - 核心处理模块
专业处理 B 站视频字幕问题，支持语音转文字、字幕下载、内容分析

更新日志：
- 2026-04-19 v2.0: 优化下载优先级（字幕→AI 字幕→音频→视频）
- 2026-04-19 v2.0: 添加系统资源检测，智能选择模型
- 2026-04-19 v1.1: 添加镜像源自动切换功能
- 2026-04-19 v1.0: 添加 Vosk 离线引擎支持
"""

import os
import sys
import json
import time
import logging
import shutil
from pathlib import Path
from typing import Dict, List, Optional, Union, Any
from dataclasses import dataclass, asdict
from datetime import datetime
import re

import requests

# 设置日志
logging.basicConfig(
    level=logging.INFO,
    format='%(asctime)s - %(name)s - %(levelname)s - %(message)s'
)
logger = logging.getLogger(__name__)


@dataclass
class VideoInfo:
    """视频信息"""
    bvid: str
    title: str
    duration: int
    up_name: str
    up_mid: str
    pubdate: int
    cid: int


@dataclass
class SubtitleResult:
    """字幕获取结果"""
    success: bool
    source: str  # "cc" / "ai" / "transcribe"
    transcript: Optional[List[Dict]] = None
    error: Optional[str] = None


@dataclass
class TranscriptSegment:
    """转录片段"""
    start: float
    end: float
    text: str
    confidence: Optional[float] = None


@dataclass
class CommentInfo:
    """评论信息"""
    user: str
    message: str
    like: int
    reply_count: int
    reply_to: Optional[str] = None  # 回复的目标用户


@dataclass
class ProcessingResult:
    """处理结果"""
    success: bool
    video_info: Optional[VideoInfo] = None
    transcript: Optional[List[TranscriptSegment]] = None
    audio_path: Optional[str] = None
    transcript_path: Optional[str] = None
    processing_time: Optional[float] = None
    error: Optional[str] = None
    warnings: Optional[List[str]] = None
    method_used: Optional[str] = None  # 使用的方法：cc_subtitle/ai_subtitle/audio_transcribe
    comments: Optional[List[CommentInfo]] = None  # 热门评论
    feishu_doc_url: Optional[str] = None  # 飞书文档链接（如已创建）


class BilibiliTranscriber:
    """B 站视频转录器"""
    
    def __init__(
        self,
        cookie_file: Optional[str] = None,
        model_name: Optional[str] = None,  # None 表示自动选择
        device: Optional[str] = None,  # None 表示自动选择
        compute_type: str = "int8",
        use_china_mirror: bool = True,
        auto_switch_mirror: bool = True,
        output_dir: str = "./bilibili_transcripts",
        keep_audio: bool = True,
        language: str = "zh",
        prefer_offline: bool = False  # 优先使用离线方式
    ):
        """
        初始化转录器
        
        Args:
            cookie_file: B 站 Cookie 文件路径
            model_name: 模型名称 (None=自动选择 / base/small/medium / vosk 路径)
            device: 设备 (None=自动选择 / cpu/cuda)
            compute_type: 计算类型 (int8/float16/float32)
            use_china_mirror: 是否使用国内镜像
            auto_switch_mirror: 是否自动切换镜像源
            output_dir: 输出目录
            keep_audio: 是否保留音频文件
            language: 语言代码
            prefer_offline: 优先使用离线方式
        """
        self.cookie_file = cookie_file
        self.output_dir = Path(output_dir)
        self.keep_audio = keep_audio
        self.language = language
        self.prefer_offline = prefer_offline
        self.auto_switch_mirror = auto_switch_mirror
        self.cookie_valid = False
        self.cookie_username = None
        self.credential = None
        
        # 自动检测系统资源并选择合适的模型
        if model_name is None or device is None:
            system_info = self._detect_system_resources()
            logger.info(f"系统资源检测结果：{system_info}")
            
            if model_name is None:
                model_name = system_info['recommended_model']
            if device is None:
                device = system_info['recommended_device']
        
        self.model_name = model_name
        self.device = device
        self.compute_type = compute_type
        
        # 镜像源列表
        self.mirrors = [
            ("原始源", "https://huggingface.co"),
            ("国内镜像", "https://hf-mirror.com"),
        ]
        
        # 设置初始镜像
        if use_china_mirror:
            os.environ['HF_ENDPOINT'] = self.mirrors[1][1]
            logger.info("使用国内镜像源：https://hf-mirror.com")
        
        # 初始化
        self.model = None
        self.credential = None
        
        # 创建输出目录
        self.output_dir.mkdir(parents=True, exist_ok=True)
        
        logger.info(f"BilibiliTranscriber 初始化完成")
        logger.info(f"模型：{model_name}, 设备：{device}, 语言：{language}")
        logger.info(f"自动切换镜像：{auto_switch_mirror}")
    
    def _detect_system_resources(self) -> Dict[str, Any]:
        """检测系统资源，推荐合适的模型"""
        import psutil
        
        # 获取 CPU 核心数
        cpu_count = psutil.cpu_count(logical=True)
        
        # 获取内存信息
        memory = psutil.virtual_memory()
        memory_gb = memory.total / (1024 ** 3)
        
        # 检测 GPU
        has_cuda = False
        try:
            import torch
            has_cuda = torch.cuda.is_available()
            if has_cuda:
                gpu_name = torch.cuda.get_device_name(0)
                gpu_memory = torch.cuda.get_device_properties(0).total_memory / (1024 ** 3)
                logger.info(f"检测到 GPU: {gpu_name} ({gpu_memory:.1f} GB)")
        except:
            pass
        
        # 检测 faster-whisper 是否已安装
        has_faster_whisper = True
        try:
            from faster_whisper import WhisperModel
        except ImportError:
            has_faster_whisper = False
            logger.warning("faster-whisper 未安装，将使用 Vosk 离线引擎")
        
        # 推荐模型策略（基于实战经验调优）
        # whisper 在低内存环境下即使 tiny 也容易 OOM
        if has_cuda and has_faster_whisper:
            recommended_device = "cuda"
            recommended_model = "medium"  # GPU 可以使用更大的模型
        elif memory_gb >= 8 and has_faster_whisper:
            recommended_device = "cpu"
            recommended_model = "base"  # 8GB+ 内存可以使用 base
        elif memory_gb >= 2 and has_faster_whisper:
            recommended_device = "cpu"
            recommended_model = "tiny"  # 2-8GB 使用 tiny
        else:
            recommended_device = "cpu"
            recommended_model = "vosk"  # <2GB 或 faster-whisper 未安装时使用 Vosk
        
        return {
            "cpu_count": cpu_count,
            "memory_gb": round(memory_gb, 2),
            "has_cuda": has_cuda,
            "has_faster_whisper": has_faster_whisper,
            "recommended_model": recommended_model,
            "recommended_device": recommended_device
        }
    
    @staticmethod
    def _sanitize_title(title: str, up_name: str, max_len: int = 80) -> str:
        """生成安全的输出目录名 {up_name}_{title}"""
        # 清理特殊字符
        name = f"{up_name}_{title}"
        name = re.sub(r'[\\/:*?"<>|]', '', name)  # 去掉 Windows 非法字符
        name = re.sub(r'[！!?？，。、：；]', '', name)  # 去掉中文标点
        name = re.sub(r'\s+', '', name)  # 去空格
        # 截断
        if len(name) > max_len:
            name = name[:max_len]
        return name
    
    def _load_cookie(self) -> Optional[str]:
        """加载 Cookie（使用 cookie_manager 冗余存储）"""
        from cookie_manager import load_cookie, check_cookie_valid, save_cookie
        
        # 1. 如果手动指定了 cookie_file，优先使用
        if self.cookie_file:
            path = Path(self.cookie_file).expanduser()
            if path.exists():
                try:
                    with open(path, 'r') as f:
                        cookie_str = f.read().strip()
                    if cookie_str:
                        # 同步到冗余存储
                        save_cookie(cookie_str)
                        self.cookie_file = str(path)
                        return cookie_str
                except Exception as e:
                    logger.warning(f"读取指定 cookie_file 失败：{e}")
        
        # 2. 使用 cookie_manager 的冗余加载
        cookie_str = load_cookie()
        if cookie_str:
            return cookie_str
        
        # 3. 检查环境变量
        env_cookie = os.environ.get('BILIBILI_COOKIE')
        if env_cookie:
            logger.info("📦 从环境变量加载 Cookie")
            return env_cookie
        
        logger.warning("⚠️ 未找到有效的 Cookie，部分功能可能受限")
        return None
    
    def _create_credential(self):
        """创建凭证（带自动验证和失效检测）"""
        from bilibili_api import Credential
        from cookie_manager import parse_cookie
        
        cookie_str = self._load_cookie()
        if not cookie_str:
            self.credential = None
            self.cookie_valid = False
            return
        
        try:
            cookies = parse_cookie(cookie_str)
            
            credential = Credential(
                sessdata=cookies.get('SESSDATA', ''),
                bili_jct=cookies.get('bili_jct', ''),
                buvid3=cookies.get('buvid3', '')
            )
            
            # 验证 Cookie 有效性
            from cookie_manager import check_cookie_valid
            check = check_cookie_valid(cookie_str)
            
            if check["valid"]:
                logger.info(f"✅ Cookie 有效 (用户: {check.get('username')}, 大会员: {check.get('is_vip')})")
                self.cookie_valid = True
                self.cookie_username = check.get('username')
            else:
                logger.warning(f"⚠️ Cookie 可能已失效: {check.get('error')}")
                self.cookie_valid = False
            
            self.credential = credential
            
        except Exception as e:
            logger.error(f"创建凭证失败：{e}")
            self.credential = None
            self.cookie_valid = False
    
    def get_comments(
        self,
        bvid: str,
        aid: int,
        max_count: int = 30,
        max_replies_per_comment: int = 3
    ) -> Optional[List[CommentInfo]]:
        """
        获取视频的热门评论（按点赞排序），以及热评下的部分回复
        
        Args:
            bvid: BV 号
            aid: 视频 aid（数字 ID）
            max_count: 最多获取多少条热评
            max_replies_per_comment: 每条热评最多获取多少条回复
            
        Returns:
            List[CommentInfo] 或 None
        """
        try:
            from bilibili_api import comment, sync
            from bilibili_api.comment import CommentResourceType, OrderType
            
            logger.info(f"📬 获取视频热门评论（最多 {max_count} 条）...")
            
            # 获取按热度排序的评论
            comments_data = sync(comment.get_comments(
                oid=aid,
                type_=CommentResourceType.VIDEO,
                page_index=1,
                order=OrderType.LIKE,
                credential=self.credential
            ))
            
            total = comments_data.get('page', {}).get('acount', 0)
            replies = comments_data.get('replies', [])
            
            if not replies:
                logger.info("📬 无评论")
                return None
            
            logger.info(f"📬 共 {total} 条评论，获取前 {min(len(replies), max_count)} 条热评")
            
            comments_list = []
            for c in replies[:max_count]:
                comment_info = CommentInfo(
                    user=c.get('member', {}).get('uname', '未知用户'),
                    message=c.get('content', {}).get('message', '').strip(),
                    like=c.get('like', 0),
                    reply_count=c.get('rcount', 0)
                )
                comments_list.append(comment_info)
                
                # 获取热评下的回复
                if max_replies_per_comment > 0 and c.get('rcount', 0) > 0:
                    try:
                        rpid = c.get('rpid', 0)
                        replies_data = sync(comment.get_comments(
                            oid=aid,
                            type_=CommentResourceType.VIDEO,
                            page_index=1,
                            order=OrderType.TIME,
                            credential=self.credential
                        ))
                        # 查找该评论的子回复
                        for reply in replies_data.get('replies', []):
                            if reply.get('parent', 0) == rpid:
                                comments_list.append(CommentInfo(
                                    user=reply.get('member', {}).get('uname', '未知'),
                                    message=reply.get('content', {}).get('message', '').strip(),
                                    like=reply.get('like', 0),
                                    reply_count=0,
                                    reply_to=c.get('member', {}).get('uname', '')
                                ))
                                if len([x for x in comments_list if x.reply_to]) >= max_replies_per_comment:
                                    break
                    except Exception as e:
                        logger.debug(f"获取评论 {c.get('rpid')} 的回复失败: {e}")
                        continue
            
            logger.info(f"✅ 成功获取 {len(comments_list)} 条评论/回复信息")
            return comments_list
            
        except Exception as e:
            logger.warning(f"获取评论失败: {e}")
            return None
    
    def get_video_info(self, bvid: str) -> Optional[VideoInfo]:
        """获取视频信息"""
        try:
            from bilibili_api import video, sync
            
            if self.credential is None:
                self._create_credential()
            
            v = video.Video(bvid=bvid, credential=self.credential)
            info = sync(v.get_info())
            pages = sync(v.get_pages())
            cid = pages[0]['cid']
            
            video_info = VideoInfo(
                bvid=bvid,
                title=info.get('title', ''),
                duration=info.get('duration', 0),
                up_name=info.get('owner', {}).get('name', ''),
                up_mid=str(info.get('owner', {}).get('mid', '')),
                pubdate=info.get('pubdate', 0),
                cid=cid
            )
            
            logger.info(f"视频信息获取成功：{video_info.title}")
            return video_info
            
        except Exception as e:
            logger.error(f"获取视频信息失败：{e}")
            return None
    
    def try_get_cc_subtitle(self, bvid: str, cid: int) -> Optional[SubtitleResult]:
        """
        第一步：尝试获取 CC 字幕
        优先级最高，因为不需要下载和转录
        """
        try:
            from bilibili_api import video, sync
            
            if self.credential is None:
                self._create_credential()
            
            v = video.Video(bvid=bvid, credential=self.credential)
            subtitle_info = sync(v.get_subtitle())
            
            subtitles = subtitle_info.get('subtitles', [])
            if not subtitles:
                logger.info("未找到 CC 字幕")
                return None
            
            logger.info(f"找到 {len(subtitles)} 个 CC 字幕轨道")
            
            # 优先选择中文字幕
            target_sub = None
            for sub in subtitles:
                if sub.get('lan') in ['zh-CN', 'zh']:
                    target_sub = sub
                    break
            
            if not target_sub:
                target_sub = subtitles[0]
            
            # 下载字幕
            subtitle_url = target_sub.get('subtitle_url', '')
            if not subtitle_url.startswith('http'):
                subtitle_url = f"https:{subtitle_url}"
            
            logger.info(f"下载 CC 字幕：{target_sub.get('lan')}")
            response = requests.get(subtitle_url, timeout=30)
            subtitle_data = response.json()
            
            # 转换为 TranscriptSegment 格式
            transcript = []
            for line in subtitle_data.get('body', []):
                transcript.append(TranscriptSegment(
                    start=line.get('from', 0),
                    end=line.get('to', 0),
                    text=line.get('content', ''),
                    confidence=1.0
                ))
            
            logger.info(f"✅ CC 字幕获取成功：{len(transcript)} 条")
            return SubtitleResult(
                success=True,
                source="cc",
                transcript=[{"start": s.start, "end": s.end, "text": s.text} for s in transcript]
            )
            
        except Exception as e:
            logger.warning(f"获取 CC 字幕失败：{e}")
            return None
    
    def try_get_ai_subtitle(self, bvid: str, cid: int) -> Optional[SubtitleResult]:
        """
        第二步：尝试获取 AI 字幕
        优先级次之，也不需要下载和转录
        """
        try:
            from bilibili_api import video, sync
            
            if self.credential is None:
                self._create_credential()
            
            v = video.Video(bvid=bvid, credential=self.credential)
            
            # 尝试获取 AI 字幕
            subtitle_info = sync(v.get_subtitle())
            subtitles = subtitle_info.get('subtitles', [])
            
            # 查找 AI 字幕
            ai_subtitle = None
            for sub in subtitles:
                if sub.get('type') == 'ai' or sub.get('lan', '').startswith('ai-'):
                    ai_subtitle = sub
                    break
            
            if not ai_subtitle:
                logger.info("未找到 AI 字幕")
                return None
            
            # 下载 AI 字幕
            subtitle_url = ai_subtitle.get('subtitle_url', '')
            if not subtitle_url.startswith('http'):
                subtitle_url = f"https:{subtitle_url}"
            
            logger.info(f"下载 AI 字幕：{ai_subtitle.get('lan')}")
            response = requests.get(subtitle_url, timeout=30)
            subtitle_data = response.json()
            
            # 转换为 TranscriptSegment 格式
            transcript = []
            for line in subtitle_data.get('body', []):
                transcript.append(TranscriptSegment(
                    start=line.get('from', 0),
                    end=line.get('to', 0),
                    text=line.get('content', ''),
                    confidence=0.95  # AI 字幕置信度略低于 CC
                ))
            
            logger.info(f"✅ AI 字幕获取成功：{len(transcript)} 条")
            return SubtitleResult(
                success=True,
                source="ai",
                transcript=[{"start": s.start, "end": s.end, "text": s.text} for s in transcript]
            )
            
        except Exception as e:
            logger.warning(f"获取 AI 字幕失败：{e}")
            return None
    
    def download_audio(self, bvid: str, video_info: VideoInfo, output_path: Path) -> Optional[str]:
        """
        第三步：下载音频文件
        只有在没有字幕的情况下才需要
        """
        try:
            from bilibili_api import video, sync
            
            if self.credential is None:
                self._create_credential()
            
            v = video.Video(bvid=bvid, credential=self.credential)
            urls = sync(v.get_download_url(page_index=0))
            
            audio_list = urls.get('dash', {}).get('audio', [])
            if not audio_list:
                logger.error("未找到音频 URL")
                return None
            
            audio_url = audio_list[0].get('baseUrl', '')
            if not audio_url:
                return None
            
            logger.info(f"音频 URL 获取成功")
            
            cookie_str = self._load_cookie()
            headers = {
                'Cookie': cookie_str if cookie_str else '',
                'User-Agent': 'Mozilla/5.0',
                'Referer': f'https://www.bilibili.com/video/{bvid}'
            }
            
            output_path.parent.mkdir(parents=True, exist_ok=True)
            
            logger.info(f"开始下载音频：{output_path}")
            session = requests.Session()
            session.headers.update(headers)
            
            response = session.get(audio_url, stream=True, timeout=30)
            response.raise_for_status()
            
            with open(output_path, 'wb') as f:
                for chunk in response.iter_content(chunk_size=8192):
                    f.write(chunk)
            
            file_size = output_path.stat().st_size
            logger.info(f"音频下载完成：{file_size/1024/1024:.2f} MB")
            
            return str(output_path)
            
        except Exception as e:
            logger.error(f"下载音频失败：{e}")
            return None
    
    def download_video(self, bvid: str, video_info: VideoInfo, output_path: Path) -> Optional[str]:
        """
        第四步：下载视频文件
        只有在无法获取音频时才需要（极少情况）
        """
        try:
            from bilibili_api import video, sync
            
            if self.credential is None:
                self._create_credential()
            
            v = video.Video(bvid=bvid, credential=self.credential)
            urls = sync(v.get_download_url(page_index=0))
            
            # 获取视频 URL
            video_list = urls.get('dash', {}).get('video', [])
            if not video_list:
                logger.error("未找到视频 URL")
                return None
            
            # 选择合适清晰度的视频
            video_url = video_list[0].get('baseUrl', '')
            if not video_url:
                return None
            
            logger.info(f"视频 URL 获取成功")
            
            cookie_str = self._load_cookie()
            headers = {
                'Cookie': cookie_str if cookie_str else '',
                'User-Agent': 'Mozilla/5.0',
                'Referer': f'https://www.bilibili.com/video/{bvid}'
            }
            
            output_path.parent.mkdir(parents=True, exist_ok=True)
            
            logger.info(f"开始下载视频：{output_path}")
            session = requests.Session()
            session.headers.update(headers)
            
            response = session.get(video_url, stream=True, timeout=60)
            response.raise_for_status()
            
            with open(output_path, 'wb') as f:
                for chunk in response.iter_content(chunk_size=8192):
                    f.write(chunk)
            
            file_size = output_path.stat().st_size
            logger.info(f"视频下载完成：{file_size/1024/1024:.2f} MB")
            
            return str(output_path)
            
        except Exception as e:
            logger.error(f"下载视频失败：{e}")
            return None
    
    def _load_model(self):
        """加载模型（Whisper 或 Vosk）"""
        if self.model is None:
            if self.model_name == "vosk":
                return self._load_vosk_model()
            else:
                if self.auto_switch_mirror:
                    self.model = self._load_model_with_retry()
                else:
                    self._load_model_simple()
    
    def _load_vosk_model(self):
        """加载 Vosk 离线模型"""
        try:
            from vosk import Model
            
            model_paths = [
                self.model_name if self.model_name != "vosk" else None,
                "/root/.cache/vosk/vosk-model-small-cn-0.22",
                "/usr/share/vosk-models/vosk-model-small-cn-0.22",
                Path.home() / ".cache/vosk/vosk-model-small-cn-0.22",
            ]
            
            model_path = None
            for path in [p for p in model_paths if p]:
                if Path(path).exists():
                    model_path = path
                    break
            
            if not model_path:
                raise FileNotFoundError("未找到 Vosk 模型")
            
            logger.info(f"加载 Vosk 模型：{model_path}")
            self.model = Model(str(model_path))
            logger.info(f"✅ Vosk 模型加载成功")
            return self.model
            
        except Exception as e:
            logger.error(f"Vosk 模型加载失败：{e}")
            raise
    
    def _load_model_simple(self):
        """简单加载 Whisper 模型"""
        logger.info(f"加载 Whisper {self.model_name} 模型...")
        try:
            from faster_whisper import WhisperModel
            self.model = WhisperModel(
                self.model_name,
                device=self.device,
                compute_type=self.compute_type
            )
            logger.info(f"模型加载成功：{self.model_name}")
        except Exception as e:
            logger.error(f"模型加载失败：{e}")
            raise
    
    def _load_model_with_retry(self):
        """加载模型，失败时自动切换镜像源"""
        from faster_whisper import WhisperModel
        
        last_error = None
        
        for name, mirror in self.mirrors:
            try:
                if mirror != "https://huggingface.co":
                    logger.info(f"🔄 切换到镜像源：{mirror} ({name})")
                    os.environ['HF_ENDPOINT'] = mirror
                else:
                    logger.info(f"尝试原始源：{mirror}")
                
                logger.info(f"加载 Whisper {self.model_name} 模型...")
                model = WhisperModel(
                    self.model_name,
                    device=self.device,
                    compute_type=self.compute_type
                )
                
                logger.info(f"✅ 模型加载成功：{self.model_name} (来源：{name})")
                return model
                
            except Exception as e:
                logger.warning(f"❌ 镜像源 {name} 失败：{e}")
                last_error = e
                continue
        
        error_msg = (
            f"所有镜像源都失败。最后错误：{last_error}\n"
            f"建议：\n"
            f"1. 检查网络连接\n"
            f"2. 使用 Vosk 离线引擎：设置 model_name='vosk'\n"
            f"3. 手动下载模型到本地"
        )
        logger.error(error_msg)
        raise Exception(error_msg)
    
    def transcribe_audio(self, audio_path: str) -> Optional[List[TranscriptSegment]]:
        """转录音频"""
        try:
            self._load_model()
            
            logger.info(f"开始转录：{audio_path}")
            start_time = time.time()
            
            if self.model_name == "vosk":
                transcript = self._transcribe_with_vosk(audio_path)
            else:
                transcript = self._transcribe_with_whisper(audio_path)
            
            processing_time = time.time() - start_time
            logger.info(f"转录完成：{len(transcript)} 个片段，耗时：{processing_time:.2f}秒")
            
            return transcript
            
        except Exception as e:
            logger.error(f"转录失败：{e}")
            return None
    
    def _transcribe_with_whisper(self, audio_path: str) -> List[TranscriptSegment]:
        """使用 Whisper 转录"""
        segments, info = self.model.transcribe(
            audio_path,
            language=self.language,
            beam_size=5,
            best_of=5,
            word_timestamps=False,
            prepend_punctuations="\"'¿([{-",
            append_punctuations="\"'.。,，!！?：:"
        )
        
        logger.info(f"语言检测：{info.language}, 置信度：{info.language_probability:.2f}")
        
        transcript = []
        for segment in segments:
            transcript.append(TranscriptSegment(
                start=segment.start,
                end=segment.end,
                text=segment.text.strip(),
                confidence=getattr(segment, 'confidence', None)
            ))
        
        return transcript
    
    def _transcribe_with_vosk(self, audio_path: str) -> List[TranscriptSegment]:
        """使用 Vosk 转录，支持分块处理避免 OOM"""
        import wave
        import subprocess
        from vosk import KaldiRecognizer
        
        logger.info(f"使用 Vosk 引擎转录：{audio_path}")
        
        # 转换为 WAV
        wav_path = str(audio_path).replace('.m4a', '_temp.wav').replace('.mp4', '_temp.wav')
        if not Path(wav_path).exists():
            subprocess.run([
                'ffmpeg', '-y', '-i', str(audio_path),
                '-vn', '-acodec', 'pcm_s16le', '-ar', '16000', '-ac', '1',
                wav_path
            ], check=True, capture_output=True)
        
        # 获取音频时长
        duration_sec = 0
        try:
            probe = subprocess.run([
                'ffprobe', '-v', 'error', '-show_entries', 'format=duration',
                '-of', 'default=noprint_wrappers=1:nokey=1', wav_path
            ], capture_output=True, text=True, timeout=15)
            if probe.stdout.strip():
                duration_sec = float(probe.stdout.strip())
        except:
            pass
        
        # 分块策略：每块最长 180 秒（适合低内存环境）
        chunk_sec = 180
        sample_rate = 16000
        chunk_frames = chunk_sec * sample_rate
        
        transcript = []
        frame_offset = 0
        chunk_idx = 0
        
        with wave.open(wav_path, "rb") as wf:
            total_frames = wf.getnframes()
            logger.info(f"WAV 文件：{total_frames} 帧 ({duration_sec:.1f}s)，"
                        f"每块 {chunk_frames} 帧 ({chunk_sec}s)，约 {(total_frames // chunk_frames) + 1} 块")
            
            while frame_offset < total_frames:
                chunk_idx += 1
                # 计算当前块的帧数
                remaining = total_frames - frame_offset
                this_chunk = min(chunk_frames, remaining)
                # 多读一点让 KaldiRecognizer 有更好的上下文
                read_size = min(this_chunk + sample_rate, remaining)
                
                logger.info(f"块 {chunk_idx}: 偏移 {frame_offset} 帧, 读取 {read_size} 帧")
                
                wf.setpos(frame_offset)
                chunk_data = wf.readframes(read_size)
                
                rec = KaldiRecognizer(self.model, sample_rate)
                rec.AcceptWaveform(chunk_data)
                
                # 收集结果
                partial_results = []
                # KaldiRecognizer 不会在中途给出结果，需要从 AcceptWaveform 获取
                result = json.loads(rec.Result())
                if result.get('text'):
                    partial_results.append(result['text'])
                
                final = json.loads(rec.FinalResult())
                if final.get('text'):
                    partial_results.append(final['text'])
                
                # 合并段落
                combined = '。'.join(partial_results)
                if combined:
                    chunk_start = frame_offset / sample_rate
                    chunk_end = min(frame_offset + read_size, total_frames) / sample_rate
                    transcript.append(TranscriptSegment(
                        start=chunk_start,
                        end=chunk_end,
                        text=combined
                    ))
                
                frame_offset += this_chunk
            
        # 清理临时文件
        try:
            Path(wav_path).unlink()
        except:
            pass
        
        logger.info(f"Vosk 转写完成：{len(transcript)} 段")
        return transcript
    
    def save_transcript(
        self,
        transcript: List[TranscriptSegment],
        video_info: VideoInfo,
        output_path: Path,
        format: str = "txt",
        comments: Optional[List[CommentInfo]] = None
    ) -> bool:
        """保存转录结果（含可选评论信息）"""
        try:
            output_path.parent.mkdir(parents=True, exist_ok=True)
            
            if format == "txt":
                lines = []
                for seg in transcript:
                    lines.append(f"[{seg.start:.2f}s -> {seg.end:.2f}s] {seg.text}")
                with open(output_path, 'w', encoding='utf-8') as f:
                    f.write('\n'.join(lines))
                
            elif format == "json":
                data = {
                    "video_info": asdict(video_info),
                    "transcript": [asdict(seg) for seg in transcript],
                    "metadata": {
                        "model": self.model_name,
                        "language": self.language,
                        "processing_time": datetime.now().isoformat()
                    }
                }
                if comments:
                    data["comments"] = [asdict(c) for c in comments]
                with open(output_path, 'w', encoding='utf-8') as f:
                    json.dump(data, f, ensure_ascii=False, indent=2)
            
            elif format == "markdown":
                lines = [
                    f"# {video_info.title}",
                    "",
                    "## 📋 视频信息",
                    "",
                    f"| 项目 | 内容 |",
                    f"|------|------|",
                    f"| **视频标题** | {video_info.title} |",
                    f"| **BV 号** | {video_info.bvid} |",
                    f"| **UP 主** | {video_info.up_name} |",
                    f"| **时长** | {video_info.duration}秒 |",
                    f"| **发布时间** | {datetime.fromtimestamp(video_info.pubdate).strftime('%Y-%m-%d %H:%M:%S')} |",
                    f"| **处理时间** | {datetime.now().strftime('%Y-%m-%d %H:%M:%S')} |",
                    "",
                ]
                
                # 转录摘要
                full_text = ''.join([seg.text for seg in transcript])
                lines.append("---")
                lines.append("")
                lines.append(f"## 📝 转录摘要")
                lines.append("")
                lines.append(f"- 总段落数：{len(transcript)}")
                lines.append(f"- 总字符数：{len(full_text)}")
                lines.append("")
                
                # 评论区信息
                if comments:
                    lines.append("---")
                    lines.append("")
                    lines.append("## 💬 热门评论")
                    lines.append("")
                    for c in comments:
                        if c.reply_to:
                            lines.append(f"> 💬 **{c.user}** 回复 **{c.reply_to}**：{c.message}")
                        else:
                            lines.append(f"### 👍 {c.like} · {c.user}")
                            lines.append("")
                            lines.append(c.message)
                            lines.append("")
                    lines.append("---")
                    lines.append("")
                
                lines.append("## 📄 完整转录")
                lines.append("")
                
                for seg in transcript:
                    lines.append(f"[{seg.start:.2f}s -> {seg.end:.2f}s] {seg.text}")
                
                with open(output_path, 'w', encoding='utf-8') as f:
                    f.write('\n'.join(lines))
            
            else:
                logger.error(f"不支持的格式：{format}")
                return False
            
            logger.info(f"转录结果保存成功：{output_path}")
            return True
            
        except Exception as e:
            logger.error(f"保存转录结果失败：{e}")
            return False

    def create_lark_doc(
        self,
        output_path: Path,
        video_info: VideoInfo,
        transcript: List[TranscriptSegment],
        comments: Optional[List[CommentInfo]] = None,
        wiki_space: Optional[str] = None,
        up_name: Optional[str] = None
    ) -> Optional[str]:
        """
        尝试创建飞书文档（使用 lark-cli）
        返回文档 URL，失败时返回 None
        
        注意：lark-cli 1.0.18 的 --markdown 参数有 bug，需使用 pipe 方式
        """
        import subprocess
        import tempfile
        
        # 生成飞书友好格式的 markdown
        pub_date = datetime.fromtimestamp(video_info.pubdate).strftime('%Y-%m-%d')
        safe_up = up_name or video_info.up_name
        doc_title = f"[视频总结] {safe_up} - {self._sanitize_title(video_info.title, safe_up, 40)}"
        
        try:
            # 先用 markdown 格式保存最完整的文档
            full_text = ''.join([seg.text for seg in transcript])
            
            lines = [
                f"## 📋 视频信息",
                "",
                f"| 项目 | 内容 |",
                f"|------|------|",
                f"| **视频标题** | {video_info.title} |",
                f"| **BV 号** | {video_info.bvid} |",
                f"| **UP 主** | {safe_up} |",
                f"| **时长** | {video_info.duration // 60}分{video_info.duration % 60}秒 |",
                f"| **发布时间** | {pub_date} |",
                f"| **原视频** | [点击观看](https://www.bilibili.com/video/{video_info.bvid}) |",
                "",
                "---",
                "",
                f"## 📝 结构化内容总结",
                "",
                f"- 总段落数：{len(transcript)}",
                f"- 总字符数：{len(full_text)}",
                "",
            ]
            
            # 按时间分段
            for i, seg in enumerate(transcript):
                start_m = int(seg.start // 60)
                start_s = int(seg.start % 60)
                end_m = int(seg.end // 60)
                end_s = int(seg.end % 60)
                time_label = f"{start_m}:{start_s:02d} - {end_m}:{end_s:02d}"
                lines.append(f"### ⏱ {time_label}")
                lines.append("")
                lines.append(f"{seg.text}")
                lines.append("")
            
            # 评论
            if comments:
                lines.append("---")
                lines.append("")
                lines.append("## 💬 热门评论")
                lines.append("")
                for c in comments[:10]:  # 最多10条
                    lines.append(f"- **{c.user}** (👍{c.like}): {c.message[:200]}")
                lines.append("")
            
            lines.append("---")
            lines.append("")
            lines.append(f"*处理时间: {datetime.now().strftime('%Y-%m-%d %H:%M:%S')}*")
            lines.append("")
            lines.append(f"> ⚠️ 注意: 本内容基于{'字幕' if self.model_name != 'vosk' else 'Vosk语音转写'}生成")
            
            md_content = '\n'.join(lines)
            
            # 使用 lark-cli 创建文档（pipe 模式避免文件名bug）
            cmd = ['lark-cli', 'docs', '+create',
                   '--title', doc_title,
                   '--markdown', '-']
            if wiki_space:
                cmd.extend(['--wiki-space', wiki_space])
            
            result = subprocess.run(
                cmd,
                input=md_content.encode('utf-8'),
                capture_output=True,
                timeout=30
            )
            
            if result.returncode == 0:
                import json
                output = result.stdout.decode('utf-8')
                json_start = output.find('{')
                if json_start >= 0:
                    resp = json.loads(output[json_start:])
                    if resp.get('ok'):
                        doc_url = resp['data'].get('doc_url', '')
                        logger.info(f"✅ 飞书文档创建成功: {doc_url}")
                        return doc_url
            
            logger.warning(f"飞书文档创建失败: {result.stderr.decode()[:200]}")
            return None
            
        except Exception as e:
            logger.warning(f"飞书文档创建异常（非关键步骤）: {e}")
            return None

    def process(
        self,
        bvid: str,
        output_format: str = "txt",
        validate: bool = True
    ) -> ProcessingResult:
        """
        处理 B 站视频 - 优化优先级版本
        
        优先级：
        1. 获取 CC 字幕（最快，无需下载）
        2. 获取 AI 字幕（次快，无需下载）
        3. 下载音频并转录（需要下载）
        4. 下载视频并提取音频（最后选择，极少使用）
        
        Args:
            bvid: B 站视频 BV 号
            output_format: 输出格式 (txt/json/markdown)
            validate: 是否验证转录内容
        
        Returns:
            ProcessingResult: 处理结果
        """
        start_time = time.time()
        warnings = []
        method_used = None
        
        try:
            logger.info(f"开始处理视频：{bvid}")
            logger.info("=" * 60)
            logger.info("处理策略：字幕优先 > AI 字幕 > 音频转录 > 视频下载")
            logger.info("=" * 60)
            
            # 获取视频信息
            video_info = self.get_video_info(bvid)
            if not video_info:
                return ProcessingResult(
                    success=False,
                    error="无法获取视频信息"
                )
            
            # 创建输出目录（使用 {up_name}_{title} 命名而非 BV 号）
            dir_name = self._sanitize_title(video_info.title, video_info.up_name)
            video_output_dir = self.output_dir / dir_name
            video_output_dir.mkdir(parents=True, exist_ok=True)
            
            transcript = None
            
            # ========== 第一步：尝试获取 CC 字幕 ==========
            logger.info("\n【步骤 1/3】尝试获取 CC 字幕...")
            subtitle_result = self.try_get_cc_subtitle(bvid, video_info.cid)
            if subtitle_result and subtitle_result.success:
                logger.info("✅ 使用 CC 字幕（无需下载和转录）")
                method_used = "cc_subtitle"
                transcript = [
                    TranscriptSegment(
                        start=s.get('start', 0),
                        end=s.get('end', 0),
                        text=s.get('text', ''),
                        confidence=1.0
                    )
                    for s in subtitle_result.transcript
                ]
            
            # ========== 第二步：尝试获取 AI 字幕 ==========
            if not transcript:
                logger.info("\n【步骤 2/3】尝试获取 AI 字幕...")
                subtitle_result = self.try_get_ai_subtitle(bvid, video_info.cid)
                if subtitle_result and subtitle_result.success:
                    logger.info("✅ 使用 AI 字幕（无需下载和转录）")
                    method_used = "ai_subtitle"
                    transcript = [
                        TranscriptSegment(
                            start=s.get('start', 0),
                            end=s.get('end', 0),
                            text=s.get('text', ''),
                            confidence=0.95
                        )
                        for s in subtitle_result.transcript
                    ]
            
            # ========== 第三步：下载音频并转录 ==========
            if not transcript:
                duration_min = video_info.duration // 60
                if duration_min > 30:
                    # 超过30分钟，提示用户确认
                    logger.info(f"\n⚠️ 视频时长 {duration_min} 分钟，超过30分钟")
                    logger.info("   下载音频并转录可能需要较长时间和存储空间")
                    logger.info("   选项：")
                    logger.info("   1 - 继续下载音频并转录")
                    logger.info("   2 - 取消处理（字幕和转录均不可用）")
                    choice = input("   请选择 (1/2，默认2): ").strip() or "2"
                    
                    if choice == "2":
                        logger.info("❌ 用户取消处理")
                        return ProcessingResult(
                            success=False,
                            error="用户取消：视频无字幕且过长，转录成本过高"
                        )
                    # choice == "1" → 继续执行转录

                
                logger.info(f"\n【步骤 3/3】下载音频并转录...")
                audio_path = video_output_dir / "audio.m4a"
                downloaded_path = self.download_audio(bvid, video_info, audio_path)
                
                if downloaded_path:
                    transcript = self.transcribe_audio(downloaded_path)
                    if transcript:
                        logger.info("✅ 使用音频转录")
                        method_used = "audio_transcribe"
            
            # 检查是否成功获取转录
            if not transcript:
                return ProcessingResult(
                    success=False,
                    error="所有方法都失败：CC 字幕、AI 字幕、音频转录"
                )
            
            # 验证转录内容
            if validate:
                transcript_text = " ".join([seg.text for seg in transcript])
                # 简单验证
                if len(transcript_text) < 50:
                    warnings.append(f"转录内容过短：{len(transcript_text)} 字")
            
            # ========== 额外步骤：获取热门评论 ==========
            comments = None
            try:
                # 获取 aid
                from bilibili_api import video as bilibili_video
                aid = None
                if self.credential:
                    import requests as req
                    info_url = f'https://api.bilibili.com/x/web-interface/view?bvid={bvid}'
                    r = req.get(info_url, headers={'User-Agent': 'Mozilla/5.0'})
                    if r.status_code == 200:
                        aid = r.json().get('data', {}).get('aid')
                
                if aid:
                    comments = self.get_comments(bvid, aid, max_count=30, max_replies_per_comment=3)
                else:
                    logger.warning("无法获取 aid，跳过评论获取")
            except Exception as e:
                logger.warning(f"获取评论失败（非关键步骤）: {e}")
            
            # 保存结果（txt + json + markdown 三种格式）
            transcript_txt = video_output_dir / "transcript.txt"
            transcript_json = video_output_dir / "transcript.json"
            transcript_md = video_output_dir / "summary.md"
            
            self.save_transcript(transcript, video_info, transcript_txt, "txt", comments=comments)
            self.save_transcript(transcript, video_info, transcript_json, "json", comments=comments)
            if not self.save_transcript(transcript, video_info, transcript_md, "markdown", comments=comments):
                logger.error("保存 markdown 失败")
            
            # 尝试创建飞书文档（非关键步骤）
            feishu_url = self.create_lark_doc(
                video_output_dir, video_info, transcript,
                comments=comments,
                up_name=video_info.up_name
            )
            if feishu_url:
                logger.info(f"📄 飞书文档已创建: {feishu_url}")
            
            # 清理临时文件
            if not self.keep_audio:
                try:
                    audio_file = video_output_dir / "audio.m4a"
                    if audio_file.exists():
                        audio_file.unlink()
                    video_file = video_output_dir / "video.mp4"
                    if video_file.exists():
                        video_file.unlink()
                    logger.info("临时文件已清理")
                except Exception as e:
                    warnings.append(f"清理临时文件失败：{e}")
            
            processing_time = time.time() - start_time
            
            result = ProcessingResult(
                success=True,
                video_info=video_info,
                transcript=transcript,
                audio_path=str(audio_path) if self.keep_audio and method_used in ["audio_transcribe", "video_transcribe"] else None,
                transcript_path=str(transcript_txt),
                processing_time=processing_time,
                warnings=warnings if warnings else None,
                method_used=method_used,
                comments=comments,
                feishu_doc_url=feishu_url
            )
            
            logger.info("\n" + "=" * 60)
            logger.info(f"✅ 视频处理完成：{bvid}")
            logger.info(f"使用方法：{method_used}")
            logger.info(f"总耗时：{processing_time:.2f}秒")
            logger.info("=" * 60)
            
            return result
            
        except Exception as e:
            logger.error(f"处理视频时发生错误：{e}")
            return ProcessingResult(
                success=False,
                error=str(e)
            )


class BilibiliLogin:
    """B 站扫码登录工具（使用 cookie_manager）"""
    
    def __init__(self):
        self.qrcode_key = None
        self.qrcode_url = None
    
    def generate_qr(self) -> str:
        """生成登录二维码，返回二维码图片路径"""
        from cookie_manager import BilibiliQRLogin
        
        login = BilibiliQRLogin()
        qr_path = login.generate_qr_code()
        self.qrcode_key = login.qrcode_key
        self.qrcode_url = login.qrcode_url
        return qr_path
    
    def poll(self) -> Dict[str, Any]:
        """轮询登录状态"""
        from cookie_manager import BilibiliQRLogin
        
        login = BilibiliQRLogin()
        login.qrcode_key = self.qrcode_key
        login.qrcode_url = self.qrcode_url
        
        result = login.poll_login(timeout_seconds=180)
        
        if result.get('success'):
            return {
                'success': True,
                'username': result.get('username', 'Unknown'),
                'is_vip': result.get('is_vip', False),
                'cookie': result.get('cookie', '')
            }
        
        return {'success': False, 'error': result.get('error', '登录失败')}


if __name__ == "__main__":
    print("B 站视频转录专家 v2.0 - 优化优先级版本")
    print("=" * 60)
    print("处理策略：字幕优先 > AI 字幕 > 音频转录 > 视频下载")
    print("=" * 60)
    
    # 示例：自动检测系统资源
    transcriber = BilibiliTranscriber(
        cookie_file="~/.bilibili_cookie.txt",
        model_name=None,  # 自动选择
        device=None  # 自动选择
    )
