import calendar
import os
import re
from datetime import datetime, timedelta
from openai import OpenAI
from dotenv import load_dotenv

from bazi_simple import bazi_dayun
from ganzhi import ten_deities, zhi5
from lunar_python import Solar
from prompt_config import CHAT_SYSTEM_PROMPT, LLM_CONFIG, PROMPT_TEMPLATES, SYSTEM_PROMPTS


class BaziAnalysisSkill:
    MISSING_BIRTH_INFO_MESSAGE = (
        "请先提供出生年月日时，这样我才能排出八字和大运后再分析。"
        "你可以按\u201c公历1992年8月9日11时50分，男/女\u201d的格式告诉我；"
        "如果是农历或闰月，也请一并说明。"
    )

    @staticmethod
    def _load_openclaw_config():
        """Fallback: read OpenClaw's own config so the skill auto-uses the same backend."""
        import json
        path = os.path.expanduser("~/.openclaw/openclaw.json")
        try:
            with open(path) as f:
                cfg = json.load(f)
        except (FileNotFoundError, json.JSONDecodeError):
            return None, None, None

        providers = cfg.get("models", {}).get("providers", {})
        defaults = cfg.get("agents", {}).get("defaults", {})
        model_cfg = defaults.get("model", {})

        # primary model e.g. "deepseek/deepseek-v4-flash"
        primary = model_cfg.get("primary", "")
        if "/" in primary:
            provider_name, model_id = primary.split("/", 1)
            provider = providers.get(provider_name, {})
        else:
            # fallback: try first available provider
            provider_name, provider = next(iter(providers.items()), (None, {}))
            model_id = primary

        api_key = (provider.get("apiKey") or
                    os.getenv("OPENCLAW_API_KEY") or
                    os.getenv("OPENAI_API_KEY"))
        base_url = (provider.get("baseUrl") or
                    os.getenv("OPENCLAW_BASE_URL") or
                    os.getenv("OPENAI_BASE_URL"))
        model = model_id or os.getenv("OPENCLAW_MODEL") or os.getenv("OPENAI_MODEL")

        return api_key, base_url, model

    PILLAR_LABELS = {
        "nian": "年柱",
        "yue": "月柱",
        "ri": "日柱",
        "shi": "时柱",
    }
    GENERAL_ANALYSIS_ACTIONS = ("分析", "看看", "看下", "看一下", "解读", "算算", "测测")
    GENERAL_ANALYSIS_SUBJECTS = ("八字", "生辰", "命盘", "命格", "排盘")
    SPECIFIC_QUESTION_KEYWORDS = (
        "事业",
        "工作",
        "财运",
        "财富",
        "赚钱",
        "感情",
        "婚姻",
        "桃花",
        "健康",
        "学业",
        "考试",
        "子女",
        "父母",
        "买房",
        "投资",
        "创业",
        "跳槽",
        "离职",
        "复合",
        "离婚",
        "今年",
        "明年",
        "哪年",
        "什么时候",
        "大运",
        "流年",
        "适合",
        "能不能",
        "会不会",
        "要不要",
        "怎么",
        "如何",
        "为什么",
    )
    TEMPORAL_QUESTION_KEYWORDS = (
        "今天",
        "明天",
        "后天",
        "昨天",
        "本月",
        "这个月",
        "下个月",
        "下月",
        "上个月",
        "今年",
        "明年",
        "后年",
        "去年",
        "下周",
        "这周",
        "什么时候",
        "哪年",
        "哪月",
        "几月",
        "几号",
        "几日",
        "预产",
        "生孩子",
    )

    def __init__(self, api_key=None, base_url=None, model=None, client=None):
        load_dotenv()
        self.api_key = (
            api_key
            or self._first_env("OPENCLAW_API_KEY", "OPENAI_API_KEY", "LLM_API_KEY")
            or self._load_openclaw_config()[0]
        )
        self.base_url = (
            base_url
            or self._first_env("OPENCLAW_BASE_URL", "OPENAI_BASE_URL", "LLM_BASE_URL")
            or self._load_openclaw_config()[1]
        )
        self.model = (
            model
            or self._first_env("OPENCLAW_MODEL", "OPENAI_MODEL", "LLM_MODEL")
            or self._load_openclaw_config()[2]
            or LLM_CONFIG["model"]
        )
        self.client = client

    @staticmethod
    def _first_env(*names):
        for name in names:
            value = os.getenv(name)
            if value:
                return value
        return None

    def _build_client(self):
        kwargs = {}
        if self.api_key:
            kwargs["api_key"] = self.api_key
        if self.base_url:
            kwargs["base_url"] = self.base_url
        try:
            return OpenAI(**kwargs)
        except Exception as exc:
            raise ValueError(
                "大模型调用未配置。请在运行环境中设置 OpenClaw/OpenAI 兼容变量，"
                "例如 OPENCLAW_API_KEY、OPENCLAW_BASE_URL、OPENCLAW_MODEL，"
                "或传入 client/api_key/base_url/model。"
            ) from exc

    @staticmethod
    def build_bazi_info_string(bazi_data, gender):
        lines = [
            "八字信息：",
            f"年柱：{bazi_data['nian']['tian_gan']['char']}{bazi_data['nian']['di_zhi']['char']}",
            f"月柱：{bazi_data['yue']['tian_gan']['char']}{bazi_data['yue']['di_zhi']['char']}",
            f"日柱：{bazi_data['ri']['tian_gan']['char']}{bazi_data['ri']['di_zhi']['char']}",
            f"时柱：{bazi_data['shi']['tian_gan']['char']}{bazi_data['shi']['di_zhi']['char']}",
            f"性别：{gender}",
            f"日主：{bazi_data['ri']['tian_gan']['char']}",
        ]
        auxiliary_info = BaziAnalysisSkill.format_bazi_auxiliary_info(bazi_data)
        if auxiliary_info:
            lines.append(auxiliary_info)
        return "\n".join(lines)

    @classmethod
    def build_bazi_data_from_zhus(cls, zhus, calculator=None):
        pillars = ("nian", "yue", "ri", "shi")
        bazi_data = {}
        for pillar, (gan, zhi) in zip(pillars, zhus):
            detail = cls.build_pillar_auxiliary_detail(gan, zhi, calculator)
            bazi_data[pillar] = {
                "tian_gan": {"char": gan},
                "di_zhi": {"char": zhi},
            }
            if detail:
                bazi_data[pillar]["tian_gan"]["shi_shen"] = detail["tian_gan_shi_shen"]
                bazi_data[pillar]["di_zhi"]["cang_gan_shi_shen"] = detail["di_zhi_cang_gan_shi_shen"]
                bazi_data[pillar]["shishen_gan"] = detail["shishen_gan"]
                bazi_data[pillar]["shishen_zhi"] = detail["shishen_zhi"]
                bazi_data[pillar]["shensha"] = detail["shensha"]
        return bazi_data

    @classmethod
    def build_pillar_auxiliary_detail(cls, gan, zhi, calculator=None):
        if calculator is None or not getattr(calculator, "me", None):
            return None

        tian_gan_shi_shen = ten_deities[calculator.me][gan]
        cang_gan_parts = [f"{cang_gan}{ten_deities[calculator.me][cang_gan]}" for cang_gan in zhi5[zhi]]
        shensha = " ".join(calculator.get_shens(gan, zhi))
        return {
            "tian_gan_shi_shen": tian_gan_shi_shen,
            "di_zhi_cang_gan_shi_shen": " ".join(cang_gan_parts),
            "shishen_gan": f"{gan}{tian_gan_shi_shen}",
            "shishen_zhi": " ".join(cang_gan_parts),
            "shensha": shensha,
        }

    @classmethod
    def format_bazi_auxiliary_info(cls, bazi_data):
        lines = []
        for pillar, label in cls.PILLAR_LABELS.items():
            pillar_data = bazi_data.get(pillar, {})
            tian_gan = pillar_data.get("tian_gan", {})
            di_zhi = pillar_data.get("di_zhi", {})
            shishen_gan = (
                pillar_data.get("shishen_gan")
                or tian_gan.get("shi_shen")
                or tian_gan.get("shishen")
            )
            shishen_zhi = (
                pillar_data.get("shishen_zhi")
                or di_zhi.get("cang_gan_shi_shen")
                or di_zhi.get("shishen")
            )
            shensha = pillar_data.get("shensha")

            detail_parts = []
            if shishen_gan:
                detail_parts.append(f"天干十神：{shishen_gan}")
            if shishen_zhi:
                detail_parts.append(f"地支藏干十神：{shishen_zhi}")
            if shensha:
                detail_parts.append(f"神煞：{shensha}")
            if detail_parts:
                lines.append(f"{label}：" + "；".join(detail_parts))

        if not lines:
            return ""
        return "八字十神与神煞：\n" + "\n".join(lines)

    @classmethod
    def build_bazi_detail_table(cls, bazi_data):
        def pillar_value(pillar, field):
            pillar_data = bazi_data.get(pillar, {})
            tian_gan = pillar_data.get("tian_gan", {})
            di_zhi = pillar_data.get("di_zhi", {})

            if field == "tian_gan":
                value = tian_gan.get("char", "")
                return f"{value}（日主）" if pillar == "ri" and value else value
            if field == "tian_gan_shi_shen":
                if pillar == "ri":
                    return "日主"
                return pillar_data.get("shishen_gan") or tian_gan.get("shi_shen") or tian_gan.get("shishen") or ""
            if field == "di_zhi":
                return di_zhi.get("char", "")
            if field == "di_zhi_shi_shen":
                return pillar_data.get("shishen_zhi") or di_zhi.get("cang_gan_shi_shen") or di_zhi.get("shishen") or ""
            if field == "shensha":
                return pillar_data.get("shensha", "")
            return ""

        def cell(value):
            text = str(value or "").strip()
            if not text:
                return "-"
            return text.replace(" ", "<br>")

        pillars = ("nian", "yue", "ri", "shi")
        rows = [
            ("天干", "tian_gan"),
            ("天干十神", "tian_gan_shi_shen"),
            ("地支", "di_zhi"),
            ("地支藏干十神", "di_zhi_shi_shen"),
            ("神煞", "shensha"),
        ]
        table = [
            "## 八字命盘详情",
            "",
            "|  | 年柱 | 月柱 | 日柱 | 时柱 |",
            "|---|---|---|---|---|",
        ]
        for label, field in rows:
            values = [cell(pillar_value(pillar, field)) for pillar in pillars]
            table.append(f"| {label} | " + " | ".join(values) + " |")
        return "\n".join(table)

    @classmethod
    def format_dayun_item(cls, dayun):
        gan_zhi = cls._format_ganzhi(cls._get_dayun_value(dayun, "gan_zhi", "ganzhi"))
        return {
            "gan_zhi": gan_zhi,
            "year": cls._get_dayun_value(dayun, "year", "start_year"),
            "age": cls._get_dayun_value(dayun, "age", "start_age"),
            "shishen_gan": cls._get_dayun_value(dayun, "shishen_gan"),
            "shishen_zhi": cls._get_dayun_value(dayun, "shishen_zhi"),
            "shensha": cls._get_dayun_value(dayun, "shensha"),
        }

    @classmethod
    def _dayun_start_year(cls, dayun):
        raw = cls._get_dayun_value(dayun, "year", "start_year")
        if raw is None or raw == "":
            return None
        try:
            return int(raw)
        except (TypeError, ValueError):
            return None

    @classmethod
    def pick_dayun_triplet_around_current_year(cls, dayuns, birth_year, current_year=None):
        """按公历年选取围绕「当前大运」的三步：上一运、当前运、下一运。"""
        if not dayuns:
            return []
        current_year = int(current_year if current_year is not None else datetime.now().year)
        birth_year = int(birth_year)

        if current_year - birth_year > 100 and len(dayuns) >= 4:
            return list(dayuns[:3])

        current_dayun_index = -1
        for i, dayun in enumerate(dayuns):
            y = cls._dayun_start_year(dayun)
            if y is None:
                continue
            if y <= current_year:
                current_dayun_index = i
            else:
                break

        if current_dayun_index == -1:
            current_dayun_index = 0

        n = len(dayuns)
        if n <= 3:
            return list(dayuns)

        ci = current_dayun_index
        if ci == 0:
            return list(dayuns[0:3])
        if ci >= n - 1:
            return list(dayuns[n - 3 : n])
        return list(dayuns[ci - 1 : ci + 2])

    @staticmethod
    def has_birth_datetime(year=None, month=None, day=None, hour=None, birth_datetime=None):
        if birth_datetime is not None:
            return True
        return all(value is not None for value in (year, month, day, hour))

    @staticmethod
    def is_female_gender(gender):
        if isinstance(gender, bool):
            return gender
        return str(gender or "").strip().lower() in {"女", "女性", "female", "f", "woman"}

    def build_analysis_inputs_from_birth(
        self,
        year=None,
        month=None,
        day=None,
        hour=None,
        minute=0,
        gender="男",
        is_lunar=False,
        leap_month=False,
        birth_datetime=None,
        reference_datetime=None,
        complete_dayun_count=10,
        dayun_list_count=3,
    ):
        if not self.has_birth_datetime(year, month, day, hour, birth_datetime):
            raise ValueError(self.MISSING_BIRTH_INFO_MESSAGE)

        if birth_datetime is not None:
            year = birth_datetime.year
            month = birth_datetime.month
            day = birth_datetime.day
            hour = birth_datetime.hour
            minute = birth_datetime.minute

        calculator = bazi_dayun()
        calculator.year = int(year)
        calculator.month = int(month)
        calculator.day = int(day)
        calculator.hour = int(hour)
        calculator.minute = int(minute or 0)
        calculator.yin = bool(is_lunar)
        calculator.runyue = bool(leap_month)
        calculator.female = self.is_female_gender(gender)

        _, zhus = calculator.get_bazi()
        full_dayun = [self.format_dayun_item(dayun) for dayun in calculator.get_dayun(n=complete_dayun_count + 1)]
        ref_year = reference_datetime.year if reference_datetime is not None else None
        dayun_window = self.pick_dayun_triplet_around_current_year(
            full_dayun, int(year), current_year=ref_year
        )
        dayun_window = dayun_window[:dayun_list_count]
        return {
            "bazi_data": self.build_bazi_data_from_zhus(zhus, calculator=calculator),
            "complete_dayun": full_dayun,
            "dayun_list": dayun_window,
            "gender": gender or "男",
        }

    @staticmethod
    def format_complete_dayun(complete_dayun):
        if not complete_dayun:
            return "未提供完整大运信息。"
        lines = []
        for i, yun in enumerate(complete_dayun, start=1):
            lines.append(BaziAnalysisSkill.format_dayun_context_line(yun, index=i))
        return "\n".join(lines)

    @staticmethod
    def _get_dayun_value(dayun, *names):
        for name in names:
            if isinstance(dayun, dict) and name in dayun:
                return dayun.get(name, "")
            if hasattr(dayun, name):
                return getattr(dayun, name)
        return ""

    @staticmethod
    def _format_ganzhi(value):
        if isinstance(value, (list, tuple)):
            return "".join(str(item) for item in value)
        return "" if value is None else str(value)

    @classmethod
    def is_default_report_request(cls, user_message):
        """判断用户是否只是在泛化地要求分析八字，而非追问具体事项。"""
        normalized = (user_message or "").strip().replace(" ", "")
        if not normalized:
            return True

        has_action = any(keyword in normalized for keyword in cls.GENERAL_ANALYSIS_ACTIONS)
        has_subject = any(keyword in normalized for keyword in cls.GENERAL_ANALYSIS_SUBJECTS)
        if not has_action:
            return False

        if any(keyword in normalized for keyword in cls.SPECIFIC_QUESTION_KEYWORDS):
            return False

        return has_subject or has_action

    @classmethod
    def format_dayun_window(cls, dayun_list):
        if not dayun_list:
            return "未提供当前三步大运信息。"
        return "\n".join(cls.format_dayun_context_line(dayun, index=i) for i, dayun in enumerate(dayun_list, start=1))

    @classmethod
    def format_dayun_context_line(cls, dayun, index=None):
        gan_zhi = cls._format_ganzhi(cls._get_dayun_value(dayun, "gan_zhi", "ganzhi"))
        year = cls._get_dayun_value(dayun, "year", "start_year")
        age = cls._get_dayun_value(dayun, "age", "start_age")
        shishen_gan = cls._get_dayun_value(dayun, "shishen_gan")
        shishen_zhi = cls._get_dayun_value(dayun, "shishen_zhi")
        shensha = cls._get_dayun_value(dayun, "shensha")

        prefix = f"{index}. " if index is not None else ""
        line = f"{prefix}{gan_zhi}（起始年份：{year}，对应年龄：{age}岁）"
        details = []
        if shishen_gan:
            details.append(f"天干十神：{shishen_gan}")
        if shishen_zhi:
            details.append(f"地支藏干十神：{shishen_zhi}")
        if shensha:
            details.append(f"神煞：{shensha}")
        if details:
            line += "；" + "；".join(details)
        return line

    @staticmethod
    def format_mingge_analysis(mingge_analysis):
        if not mingge_analysis:
            return "未提供。"

        if isinstance(mingge_analysis, str):
            return mingge_analysis

        lines = []
        if mingge_analysis.get("shengchen"):
            lines.append(f"生辰解读：{mingge_analysis['shengchen']}")
        if mingge_analysis.get("shishen"):
            lines.append(f"十神格局：{mingge_analysis['shishen']}")
        if mingge_analysis.get("xiji"):
            lines.append(f"五行喜忌：{mingge_analysis['xiji']}")
        if mingge_analysis.get("element_like"):
            lines.append("喜用五行：" + "、".join(mingge_analysis["element_like"]))
        if mingge_analysis.get("element_dislike"):
            lines.append("忌讳五行：" + "、".join(mingge_analysis["element_dislike"]))
        return "\n".join(lines) if lines else "未提供。"

    @staticmethod
    def build_current_time_context():
        now = datetime.now()
        return (
            "当前时序信息：\n"
            f"当前公历日期：{now:%Y-%m-%d}\n"
            "本月干支：请由调用侧传入或在业务层补充\n"
            "今日干支：请由调用侧传入或在业务层补充"
        )

    @staticmethod
    def add_months(value, months):
        month_index = value.month - 1 + months
        year = value.year + month_index // 12
        month = month_index % 12 + 1
        day = min(value.day, calendar.monthrange(year, month)[1])
        return value.replace(year=year, month=month, day=day)

    @classmethod
    def question_has_time_reference(cls, user_message):
        normalized = (user_message or "").strip()
        if not normalized:
            return False
        if any(keyword in normalized for keyword in cls.TEMPORAL_QUESTION_KEYWORDS):
            return True
        return bool(
            re.search(r"\d{4}\s*年", normalized)
            or re.search(r"\d{1,2}\s*月\s*\d{1,2}\s*[日号]?", normalized)
        )

    @classmethod
    def resolve_target_datetime(cls, user_message, reference_datetime=None):
        reference = reference_datetime or datetime.now()
        text = (user_message or "").strip()

        match = re.search(r"(\d{4})\s*年\s*(\d{1,2})\s*月\s*(\d{1,2})\s*[日号]?", text)
        if match:
            year, month, day = (int(match.group(i)) for i in range(1, 4))
            return reference.replace(year=year, month=month, day=day), "按用户提供的具体年月日推算。"

        match = re.search(r"(\d{4})\s*年\s*(\d{1,2})\s*月", text)
        if match:
            year, month = (int(match.group(i)) for i in range(1, 3))
            day = min(reference.day, calendar.monthrange(year, month)[1])
            return reference.replace(year=year, month=month, day=day), "用户只提供到月份，按当前日期的同一日估算。"

        match = re.search(r"(\d{1,2})\s*月\s*(\d{1,2})\s*[日号]?", text)
        if match:
            month, day = (int(match.group(i)) for i in range(1, 3))
            return reference.replace(month=month, day=day), "用户未提供年份，按当前年份推算。"

        if "后天" in text:
            return reference + timedelta(days=2), "按当前日期后推两天。"
        if "明天" in text:
            return reference + timedelta(days=1), "按当前日期后推一天。"
        if "昨天" in text:
            return reference - timedelta(days=1), "按当前日期前推一天。"
        if "下周" in text:
            return reference + timedelta(days=7), "按当前日期后推一周。"
        if "下个月" in text or "下月" in text:
            return cls.add_months(reference, 1), "用户只说下个月，按当前日期顺延一个月估算。"
        if "上个月" in text:
            return cls.add_months(reference, -1), "用户只说上个月，按当前日期前推一个月估算。"
        if "明年" in text:
            return cls.add_months(reference, 12), "用户只说到明年，按当前月日顺延一年估算。"
        if "后年" in text:
            return cls.add_months(reference, 24), "用户只说到后年，按当前月日顺延两年估算。"
        if "去年" in text:
            return cls.add_months(reference, -12), "用户只说到去年，按当前月日前推一年估算。"

        return reference, "用户问题涉及时间但未给出具体日期，按当前日期估算。"

    @staticmethod
    def _to_int(value):
        try:
            return int(value)
        except (TypeError, ValueError):
            return None

    @classmethod
    def find_dayun_for_year(cls, dayun_candidates, target_year):
        if not dayun_candidates:
            return None

        active_dayun = None
        for dayun in dayun_candidates:
            start_year = cls._to_int(cls._get_dayun_value(dayun, "year", "start_year"))
            if start_year is None:
                continue
            if start_year <= target_year:
                active_dayun = dayun
            else:
                break

        return active_dayun or dayun_candidates[0]

    @classmethod
    def format_flow_ganzhi(cls, label, gan_zhi, day_master=None):
        parts = [f"{label}干支：{gan_zhi}"]
        if day_master and gan_zhi and len(gan_zhi) >= 2:
            gan = gan_zhi[0]
            zhi = gan_zhi[1]
            shishen_gan = f"{gan}{ten_deities[day_master][gan]}"
            shishen_zhi = " ".join(f"{cang_gan}{ten_deities[day_master][cang_gan]}" for cang_gan in zhi5[zhi])
            parts.append(f"天干十神：{shishen_gan}")
            parts.append(f"地支藏干十神：{shishen_zhi}")
        return "；".join(parts)

    def build_temporal_context_for_question(
        self,
        user_message,
        bazi_data,
        complete_dayun=None,
        dayun_list=None,
        reference_datetime=None,
    ):
        if not self.question_has_time_reference(user_message):
            return ""

        target_datetime, note = self.resolve_target_datetime(user_message, reference_datetime=reference_datetime)
        lunar = Solar.fromYmdHms(
            target_datetime.year,
            target_datetime.month,
            target_datetime.day,
            target_datetime.hour,
            target_datetime.minute,
            target_datetime.second,
        ).getLunar()
        day_master = bazi_data["ri"]["tian_gan"]["char"]
        dayun_candidates = complete_dayun or dayun_list or []
        active_dayun = self.find_dayun_for_year(dayun_candidates, target_datetime.year)

        lines = [
            "时间问题补充信息：",
            f"目标公历日期：{target_datetime:%Y-%m-%d}",
            f"时间解析说明：{note}",
        ]
        if active_dayun:
            lines.append("目标日期所属大运：" + self.format_dayun_context_line(active_dayun))
        else:
            lines.append("目标日期所属大运：未提供可判断的大运信息")

        lines.extend(
            [
                self.format_flow_ganzhi("流年", lunar.getYearInGanZhi(), day_master=day_master),
                self.format_flow_ganzhi("流月", lunar.getMonthInGanZhi(), day_master=day_master),
                self.format_flow_ganzhi("流日", lunar.getDayInGanZhi(), day_master=day_master),
            ]
        )
        return "\n".join(lines)

    def build_chat_context_string(
        self,
        bazi_data,
        gender,
        da_yun=None,
        complete_dayun=None,
        mingge_analysis=None,
        current_month_ganzhi=None,
        current_day_ganzhi=None,
    ):
        parts = [self.build_bazi_info_string(bazi_data, gender)]
        parts.append(
            "当前时序信息：\n"
            f"当前公历日期：{datetime.now():%Y-%m-%d}\n"
            f"本月干支：{current_month_ganzhi or '未提供'}\n"
            f"今日干支：{current_day_ganzhi or '未提供'}"
        )
        if complete_dayun:
            parts.append("完整大运（10步）：\n" + self.format_complete_dayun(complete_dayun))
        if da_yun:
            lines = ["当前展示大运："]
            for y in da_yun:
                lines.append("- " + self.format_dayun_context_line(y))
            parts.append("\n".join(lines))
        if mingge_analysis:
            parts.append("命格分析结果：\n" + self.format_mingge_analysis(mingge_analysis))
        return "\n\n".join(parts)

    def _chat(self, system_prompt, user_prompt, temperature=None):
        if not self.model:
            raise ValueError("大模型 model 未配置，请设置 OPENCLAW_MODEL、OPENAI_MODEL 或 LLM_MODEL。")
        if self.client is None:
            self.client = self._build_client()
        response = self.client.chat.completions.create(
            model=self.model,
            messages=[
                {"role": "system", "content": system_prompt},
                {"role": "user", "content": user_prompt},
            ],
            temperature=LLM_CONFIG["temperature"] if temperature is None else temperature,
            stream=False,
            timeout=LLM_CONFIG["timeout"],
        )
        return response.choices[0].message.content or ""

    def build_bazi_analysis_prompt(self, bazi_info, complete_dayun=None):
        return PROMPT_TEMPLATES["bazi_analysis"].format(
            bazi_info=bazi_info,
            complete_dayun=self.format_complete_dayun(complete_dayun),
        )

    def build_dayun_analysis_prompt(self, bazi_info, dayun_ganzhi, complete_dayun=None):
        return PROMPT_TEMPLATES["dayun_analysis"].format(
            bazi_info=bazi_info,
            dayun_ganzhi=dayun_ganzhi,
            complete_dayun=self.format_complete_dayun(complete_dayun),
        )

    def build_default_report_prompt(
        self,
        bazi_info,
        complete_dayun=None,
        dayun_list=None,
        mingge_analysis=None,
    ):
        return PROMPT_TEMPLATES["default_report"].format(
            bazi_info=bazi_info,
            complete_dayun=self.format_complete_dayun(complete_dayun),
            dayun_list=self.format_dayun_window(dayun_list),
            existing_mingge_analysis=self.format_mingge_analysis(mingge_analysis),
        )

    def parse_ai_analysis(self, content):
        analysis = {"shengchen": "", "shishen": "", "xiji": "", "element_like": [], "element_dislike": []}
        lines = [l.strip() for l in content.split("\n") if l.strip()]
        section = None
        buf = []

        def flush():
            if section and buf:
                analysis[section] = " ".join(buf).strip()

        for line in lines:
            if "1. 生辰解读" in line:
                flush()
                section = "shengchen"
                buf = [line.split("：", 1)[-1].strip()] if "：" in line else []
                continue
            if "2. 十神格局" in line:
                flush()
                section = "shishen"
                buf = [line.split("：", 1)[-1].strip()] if "：" in line else []
                continue
            if "3. 五行喜忌" in line:
                flush()
                section = "xiji"
                buf = [line.split("：", 1)[-1].strip()] if "：" in line else []
                continue
            if "【五行喜忌】" in line:
                flush()
                section = None
                buf = []
                continue
            if line.startswith("喜用五行："):
                for c in line:
                    if c in ["金", "木", "水", "火", "土"]:
                        analysis["element_like"].append(c)
                continue
            if line.startswith("忌讳五行："):
                for c in line:
                    if c in ["金", "木", "水", "火", "土"]:
                        analysis["element_dislike"].append(c)
                continue
            if section:
                buf.append(line)
        flush()
        analysis["element_like"] = sorted(set(analysis["element_like"]))
        analysis["element_dislike"] = sorted(set(analysis["element_dislike"]))
        return analysis

    def analyze_mingge(self, bazi_data, gender, complete_dayun=None):
        bazi_info = self.build_bazi_info_string(bazi_data, gender)
        prompt = self.build_bazi_analysis_prompt(bazi_info, complete_dayun=complete_dayun)
        content = self._chat(SYSTEM_PROMPTS["bazi_analysis"], prompt)
        return self.parse_ai_analysis(content)

    def analyze_dayun_detail(self, bazi_data, gan_zhi, gender="男", complete_dayun=None):
        bazi_info = self.build_bazi_info_string(bazi_data, gender)
        prompt = self.build_dayun_analysis_prompt(bazi_info, gan_zhi, complete_dayun=complete_dayun)
        content = self._chat(SYSTEM_PROMPTS["bazi_analysis"], prompt)
        return content

    def analyze_default_report(
        self,
        bazi_data,
        gender,
        complete_dayun=None,
        dayun_list=None,
        da_yun=None,
        mingge_analysis=None,
    ):
        bazi_info = self.build_bazi_info_string(bazi_data, gender)
        report_dayun_list = dayun_list if dayun_list is not None else da_yun
        prompt = self.build_default_report_prompt(
            bazi_info,
            complete_dayun=complete_dayun,
            dayun_list=report_dayun_list,
            mingge_analysis=mingge_analysis,
        )
        report = self._chat(SYSTEM_PROMPTS["default_report"], prompt)
        return f"{self.build_bazi_detail_table(bazi_data)}\n\n{report}"

    def answer_chat_question(
        self,
        user_message,
        bazi_data,
        gender,
        da_yun=None,
        complete_dayun=None,
        mingge_analysis=None,
        current_month_ganzhi=None,
        current_day_ganzhi=None,
        temporal_context=None,
    ):
        context = self.build_chat_context_string(
            bazi_data=bazi_data,
            gender=gender,
            da_yun=da_yun,
            complete_dayun=complete_dayun,
            mingge_analysis=mingge_analysis,
            current_month_ganzhi=current_month_ganzhi,
            current_day_ganzhi=current_day_ganzhi,
        )
        if temporal_context:
            context = f"{context}\n\n{temporal_context}"
            temporal_answer_instruction = (
                "时间问题补充信息只作为内部分析依据。回答时不要在开头机械列出"
                "“当前大运、流年、流月、流日、目标日期”等清单，也不要先说明按哪一天看；"
                "可以在解释原因时自然引用少量关键干支或十神，例如“丁亥日让主观性更强”。"
            )
        else:
            temporal_answer_instruction = ""
        prompt = (
            f"{context}\n\n"
            f"用户问题：{user_message}\n\n"
            "请结合以上 /chat 上下文回答用户的具体问题。只围绕问题本身分析，"
            "不要重新输出完整命格报告。"
            f"{temporal_answer_instruction}"
        )
        return self._chat(CHAT_SYSTEM_PROMPT, prompt)

    def analyze_user_request(
        self,
        user_message,
        bazi_data=None,
        gender=None,
        dayun_list=None,
        da_yun=None,
        complete_dayun=None,
        mingge_analysis=None,
        current_month_ganzhi=None,
        current_day_ganzhi=None,
        birth_year=None,
        birth_month=None,
        birth_day=None,
        birth_hour=None,
        birth_minute=0,
        birth_datetime=None,
        is_lunar=False,
        leap_month=False,
        reference_datetime=None,
    ):
        if bazi_data is None:
            if not self.has_birth_datetime(
                birth_year,
                birth_month,
                birth_day,
                birth_hour,
                birth_datetime=birth_datetime,
            ):
                return self.MISSING_BIRTH_INFO_MESSAGE

            birth_inputs = self.build_analysis_inputs_from_birth(
                year=birth_year,
                month=birth_month,
                day=birth_day,
                hour=birth_hour,
                minute=birth_minute,
                gender=gender or "男",
                is_lunar=is_lunar,
                leap_month=leap_month,
                birth_datetime=birth_datetime,
                reference_datetime=reference_datetime,
            )
            bazi_data = birth_inputs["bazi_data"]
            gender = birth_inputs["gender"]
            if complete_dayun is None:
                complete_dayun = birth_inputs["complete_dayun"]
            if dayun_list is None and da_yun is None:
                dayun_list = birth_inputs["dayun_list"]

        gender = gender or "未提供"
        active_dayun_list = dayun_list if dayun_list is not None else da_yun
        if self.is_default_report_request(user_message):
            return self.analyze_default_report(
                bazi_data=bazi_data,
                gender=gender,
                complete_dayun=complete_dayun,
                dayun_list=active_dayun_list,
                mingge_analysis=mingge_analysis,
            )

        temporal_context = self.build_temporal_context_for_question(
            user_message=user_message,
            bazi_data=bazi_data,
            complete_dayun=complete_dayun,
            dayun_list=active_dayun_list,
            reference_datetime=reference_datetime,
        )
        return self.answer_chat_question(
            user_message=user_message,
            bazi_data=bazi_data,
            gender=gender,
            da_yun=active_dayun_list,
            complete_dayun=complete_dayun,
            mingge_analysis=mingge_analysis,
            current_month_ganzhi=current_month_ganzhi,
            current_day_ganzhi=current_day_ganzhi,
            temporal_context=temporal_context,
        )

