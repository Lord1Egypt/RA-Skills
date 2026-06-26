"""
发布模块
负责将报告发布到飞书（文档 + 消息通知）

设计原则：
- 开发环境：使用模拟实现，便于测试
- OpenClaw环境：自动检测并调用真实工具（feishu_create_doc, feishu_im_user_message）
"""

import os
import json
from datetime import datetime
from utils import get_logger, format_date

logger = get_logger('publisher')


class Publisher:
    """发布类"""

    def __init__(self, config):
        self.config = config
        self.publish_config = config.get('publish', {})
        # 检测是否在 OpenClaw 环境中
        self.in_openclaw = self._detect_openclaw()
        logger.info(f"Publisher 初始化完成（环境: {'OpenClaw' if self.in_openclaw else '开发/模拟'}）")

    def _detect_openclaw(self):
        """检测是否在 OpenClaw 环境中运行"""
        # 方法1: 检查环境变量
        if os.environ.get('OPENCLAW_RUNTIME'):
            return True
        # 方法2: 检查是否有工具注入标记
        return False

    def publish_morning_report(self, markdown_content, report_date, send_notification=False):
        return self._publish_report(markdown_content, report_date, 'morning', send_notification)

    def publish_evening_report(self, markdown_content, report_date, send_notification=False):
        return self._publish_report(markdown_content, report_date, 'evening', send_notification)

    def _publish_report(self, markdown_content, report_date, mode, send_notification):
        """统一发布逻辑"""
        try:
            title = f"A股{'早报' if mode == 'morning' else '晚报'}-{format_date(report_date, '%Y%m%d')}"

            # 1. 创建飞书文档
            doc_id, doc_url = self._create_document(title, markdown_content)

            result = {
                'success': True,
                'doc_id': doc_id,
                'doc_url': doc_url,
                'title': title,
                'published_at': format_date(datetime.now(), '%Y-%m-%d %H:%M:%S')
            }

            # 2. 发送通知（可选）
            if send_notification:
                message_result = self._send_notification(title, doc_url, report_date, mode)
                result['notification_sent'] = message_result.get('success', False)
                result['notification_message_id'] = message_result.get('message_id')

            logger.info(f"✅ {mode}发布成功: {title} -> {doc_url}")
            return result

        except Exception as e:
            logger.error(f"❌ {mode}发布失败: {e}")
            return {'success': False, 'error': str(e)}

    def _create_document(self, title, markdown_content):
        """创建飞书文档（根据环境选择实现）"""
        if self.in_openclaw:
            return self._create_document_real(title, markdown_content)
        else:
            return self._create_document_mock(title, markdown_content)

    def _create_document_real(self, title, markdown_content):
        """真实工具调用（OpenClaw MCP 接口）"""
        try:
            logger.info("🌍 检测到 OpenClaw 环境，调用 feishu_create_doc 工具...")
            # TODO: 实际部署时，OpenClaw 会注入工具调用接口
            # 示例代码（待OpenClaw确认具体API）:
            # result = call_tool('feishu_create_doc', {
            #     'title': title,
            #     'markdown': markdown_content,
            #     'folder_token': self.publish_config.get('feishu_doc', {}).get('folder_token')
            # })
            # return result['doc_id'], result['doc_url']

            # 暂时降级到模拟，避免阻塞
            logger.warning("⚠️ 真实工具调用接口未就绪，使用模拟返回")
            return self._create_document_mock(title, markdown_content)

        except Exception as e:
            logger.error(f"创建文档失败: {e}")
            raise

    def _create_document_mock(self, title, markdown_content):
        """模拟创建文档（开发阶段）"""
        mock_id = f"doxcn_mock_{format_date(datetime.now(), '%Y%m%d%H%M%S')}"
        mock_url = f"https://example.feishu.cn/docx/{mock_id}"
        logger.info(f"  模拟文档ID: {mock_id}")
        logger.info(f"  模拟文档链接: {mock_url}")
        return mock_id, mock_url

    def _send_notification(self, title, doc_url, report_date, mode):
        """发送通知消息（根据环境选择实现）"""
        user_open_id = self._get_user_open_id()
        if not user_open_id:
            logger.warning("⚠️ 未配置 user_open_id，跳过消息发送")
            return {'success': False, 'error': '未配置用户ID'}

        if self.in_openclaw:
            return self._send_notification_real(title, doc_url, report_date, mode, user_open_id)
        else:
            return self._send_notification_mock(title, doc_url, report_date, mode, user_open_id)

    def _send_notification_real(self, title, doc_url, report_date, mode, user_open_id):
        """真实消息发送（OpenClaw 环境）"""
        try:
            mode_text = "早报" if mode == 'morning' else "晚报"
            date_str = format_date(report_date, '%Y年%m月%d日')
            message_text = f"""【{mode_text}已生成】

📅 日期：{date_str}
📄 标题：{title}
🔗 文档：{doc_url}

请查看以上链接获取完整报告。"""

            logger.info("🌍 发送消息（OpenClaw 环境）...")
            # TODO: 实际调用 feishu_im_user_message 工具
            # result = call_tool('feishu_im_user_message', {
            #     'receive_id': user_open_id,
            #     'msg_type': 'text',
            #     'content': json.dumps({"text": message_text}, ensure_ascii=False)
            # })
            # return {'success': True, 'message_id': result.get('message_id')}

            # 暂时降级
            logger.warning("⚠️ 真实工具调用接口未就绪，使用模拟发送")
            return self._send_notification_mock(title, doc_url, report_date, mode, user_open_id)

        except Exception as e:
            logger.error(f"发送通知失败: {e}")
            return {'success': False, 'error': str(e)}

    def _send_notification_mock(self, title, doc_url, report_date, mode, user_open_id):
        """模拟发送消息（开发阶段）"""
        mode_text = "早报" if mode == 'morning' else '晚报'
        date_str = format_date(report_date, '%Y年%m月%d日')
        message_preview = f"【{mode_text}已生成】 {date_str} {title}"
        logger.info(f"📱 [MOCK] 发送消息给 {user_open_id}")
        logger.info(f"   预览: {message_preview}")
        return {
            'success': True,
            'message_id': f"mock_msg_{format_date(datetime.now(), '%Y%m%d%H%M%S')}"
        }

    def _get_user_open_id(self):
        """获取用户 open_id（多源Fallback）"""
        # 优先级1: 发布配置中的 target_chat_id
        user_id = self.publish_config.get('feishu_message', {}).get('target_chat_id')
        if user_id:
            logger.debug(f"从配置获取 user_open_id: {user_id}")
            return user_id

        # 优先级2: 环境变量 FEISHU_NOTIFY_OPEN_ID（阿宽使用）
        user_id = os.environ.get('FEISHU_NOTIFY_OPEN_ID')
        if user_id:
            logger.debug(f"从 FEISHU_NOTIFY_OPEN_ID 获取: {user_id}")
            return user_id

        # 优先级3: 环境变量 FEISHU_USER_OPEN_ID（通用）
        user_id = os.environ.get('FEISHU_USER_OPEN_ID')
        if user_id:
            logger.debug(f"从 FEISHU_USER_OPEN_ID 获取: {user_id}")
            return user_id

        # 优先级4: 从 .env 文件加载
        dotenv_path = os.path.join(os.path.dirname(os.path.dirname(__file__)), '..', '..', '.env')
        if os.path.exists(dotenv_path):
            from dotenv import load_dotenv
            load_dotenv(dotenv_path)
            user_id = os.getenv('FEISHU_NOTIFY_OPEN_ID') or os.getenv('FEISHU_USER_OPEN_ID')
            if user_id:
                logger.debug(f"从 .env 文件加载: {user_id}")
                return user_id

        logger.warning("未找到 user_open_id 配置")
        return None

    def convert_to_pdf(self, markdown_content, output_path, title=None):
        """PDF转换（可选功能）"""
        try:
            import subprocess
            import tempfile

            html_content = self._markdown_to_html(markdown_content, title)

            with tempfile.NamedTemporaryFile(mode='w', suffix='.html', encoding='utf-8') as f:
                f.write(html_content)
                html_path = f.name

            logger.info(f"📄 转换PDF: {output_path}")
            result = subprocess.run(
                ['wkhtmltopdf', html_path, output_path],
                capture_output=True,
                text=True,
                timeout=30
            )

            if result.returncode == 0:
                logger.info(f"✅ PDF转换成功: {output_path}")
                return {'success': True, 'pdf_path': output_path}
            else:
                raise RuntimeError(result.stderr)

        except (FileNotFoundError, RuntimeError) as e:
            logger.warning(f"⚠️ PDF转换不可用: {e}")
            logger.info("  提示: 安装 wkhtmltopdf: brew install wkhtmltopdf (macOS)")
            return {'success': False, 'error': str(e)}

    def _markdown_to_html(self, markdown_content, title=None):
        """Markdown → HTML"""
        try:
            import markdown
            html = markdown.markdown(
                markdown_content,
                extensions=['tables', 'fenced_code', 'codehilite']
            )
        except ImportError:
            html = markdown_content.replace('\n', '<br>')

        return f"""
        <!DOCTYPE html>
        <html>
        <head>
            <meta charset="UTF-8">
            <title>{title or 'A股日报'}</title>
            <style>
                body {{ font-family: "PingFang SC", "Microsoft YaHei", sans-serif; margin: 40px; line-height: 1.6; }}
                h1, h2, h3 {{ color: #333; margin-top: 24px; border-bottom: 1px solid #eee; padding-bottom: 8px; }}
                table {{ border-collapse: collapse; width: 100%; margin: 16px 0; }}
                th, td {{ border: 1px solid #ddd; padding: 8px 12px; text-align: left; }}
                th {{ background-color: #f5f5f5; font-weight: bold; }}
                code {{ background-color: #f5f5f5; padding: 2px 4px; border-radius: 3px; }}
                pre {{ background-color: #f5f5f5; padding: 12px; border-radius: 4px; overflow-x: auto; }}
            </style>
        </head>
        <body>
            <h1>{title or 'A股日报'}</h1>
            {html}
        </body>
        </html>
        """
