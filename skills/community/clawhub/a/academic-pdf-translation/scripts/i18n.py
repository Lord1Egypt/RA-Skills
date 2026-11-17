from __future__ import annotations


MESSAGES = {
    "en": {
        "pdf_subject": "Target-language academic reading copy",
        "reading_version": "Translated reading version",
        "image_text_legend": "Translated text in the figure",
        "source_page": "Source page {page}",
        "over_time": "Over time",
        "retained_references": "References (entries retained in the source language)",
    },
    "zh-Hans": {
        "pdf_subject": "目标语言学术阅读译版候选",
        "reading_version": "中文译制阅读版",
        "image_text_legend": "图内文字对照",
        "source_page": "原文第 {page} 页",
        "over_time": "随时间",
        "retained_references": "参考文献（题录保留原文）",
    },
    "zh-Hant": {
        "pdf_subject": "目標語言學術閱讀譯版候選",
        "reading_version": "繁體中文譯製閱讀版",
        "image_text_legend": "圖中文字對照",
        "source_page": "原文第 {page} 頁",
        "over_time": "隨時間",
        "retained_references": "參考文獻（題錄保留原文）",
    },
    "ja": {
        "pdf_subject": "対象言語の学術閲覧用翻訳版",
        "reading_version": "翻訳閲覧版",
        "image_text_legend": "図中文字の翻訳",
        "source_page": "原文 {page} ページ",
        "over_time": "時間経過",
        "retained_references": "参考文献（書誌情報は原文のまま）",
    },
    "ko": {
        "pdf_subject": "대상 언어 학술 읽기 번역본",
        "reading_version": "번역 읽기본",
        "image_text_legend": "그림 속 번역문",
        "source_page": "원문 {page}쪽",
        "over_time": "시간 경과",
        "retained_references": "참고문헌(서지 정보는 원문 유지)",
    },
    "fr": {
        "pdf_subject": "Version académique traduite pour la lecture",
        "reading_version": "Version de lecture traduite",
        "image_text_legend": "Texte traduit dans la figure",
        "source_page": "Page source {page}",
        "over_time": "Au fil du temps",
        "retained_references": "Références (notices conservées dans la langue source)",
    },
    "de": {
        "pdf_subject": "Übersetzte akademische Lesefassung",
        "reading_version": "Übersetzte Lesefassung",
        "image_text_legend": "Übersetzter Text in der Abbildung",
        "source_page": "Quellseite {page}",
        "over_time": "Im Zeitverlauf",
        "retained_references": "Literaturverzeichnis (Angaben in der Ausgangssprache)",
    },
    "es": {
        "pdf_subject": "Versión académica traducida para lectura",
        "reading_version": "Versión de lectura traducida",
        "image_text_legend": "Texto traducido de la figura",
        "source_page": "Página original {page}",
        "over_time": "A lo largo del tiempo",
        "retained_references": "Referencias (datos conservados en el idioma original)",
    },
}


def language_key(target_language: str) -> str:
    value = str(target_language or "").strip()
    if value in MESSAGES:
        return value
    prefix = value.split("-", 1)[0]
    return prefix if prefix in MESSAGES else "en"


def message(target_language: str, key: str, **values: object) -> str:
    language = language_key(target_language)
    template = MESSAGES.get(language, MESSAGES["en"]).get(
        key,
        MESSAGES["en"][key],
    )
    return template.format(**values)


def all_messages(key: str) -> set[str]:
    return {
        values[key]
        for values in MESSAGES.values()
        if key in values
    }
