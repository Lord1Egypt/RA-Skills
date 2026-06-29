#!/usr/bin/env python3
"""Initialize a private Family OS workspace."""

from __future__ import annotations

import argparse
import locale
import os
import shutil
from datetime import datetime
from pathlib import Path


DEFAULT_CONFIG = Path.home() / ".family-os" / "config.yaml"
DEFAULT_WORKSPACE = Path.home() / "family-os-workspace"

DIRS = [
    "00-inbox",
    "01-dashboard",
    "02-areas/finance",
    "02-areas/parenting",
    "02-areas/health",
    "02-areas/career-and-income",
    "02-areas/home-and-logistics",
    "02-areas/housing-and-city",
    "02-areas/insurance",
    "02-areas/education",
    "02-areas/legal-and-admin",
    "02-areas/relationships",
    "03-projects",
    "04-decisions",
    "05-memory",
    "90-reviews/weekly",
    "90-reviews/monthly",
    "90-reviews/yearly",
    "99-archive",
]

TEXT = {
    "en": {
        "workspace_title": "Family OS Workspace",
        "workspace_intro": "This is a private household workspace. Keep personal household information here, not in the Family OS skill package.",
        "flow_title": "Main Flow",
        "flow": [
            "Put raw material in `00-inbox/`.",
            "Keep current priorities in `01-dashboard/`.",
            "Store long-running domains in `02-areas/`.",
            "Track time-bound efforts in `03-projects/`.",
            "Record durable choices in `04-decisions/`.",
            "Preserve stable facts and preferences in `05-memory/`.",
            "Review periodically in `90-reviews/`.",
            "Archive old material in `99-archive/`.",
        ],
        "overview": "Household Overview",
        "updated": "Last updated:",
        "stage": "Current Stage",
        "snapshot": "Household Snapshot",
        "principles": "Operating Principles",
        "areas": "Active Areas",
        "projects": "Active Projects",
        "priorities": "Current Priorities",
        "month": "This Month",
        "month_label": "Month:",
        "focus": "Focus",
        "calendar": "Calendar Notes",
        "money": "Money Notes",
        "logistics": "Family Logistics",
        "review": "Review Notes",
        "risks_reminders": "Risks And Reminders",
        "risks": "Risks",
        "reminders": "Reminders",
        "watch": "Watch List",
        "facts": "Household Facts",
        "facts_hint": "Use short dated entries. Mark uncertain facts as `to confirm`.",
        "values": "Family Values",
        "values_hint": "Record durable principles, tradeoffs, and values that should guide decisions.",
        "preferences": "Preferences",
        "preferences_hint": "Record recurring household preferences and defaults.",
        "people": "Important People",
        "people_hint": "Record important people and relationship context only with appropriate privacy care.",
    },
    "zh": {
        "workspace_title": "Family OS 家庭工作区",
        "workspace_intro": "这是一个私有家庭工作区。家庭资料只保存在这里，不写入 Family OS 技能包。",
        "flow_title": "使用流程",
        "flow": [
            "原始资料先放入 `00-inbox/`。",
            "当前重点维护在 `01-dashboard/`。",
            "长期领域沉淀在 `02-areas/`。",
            "阶段性事务推进在 `03-projects/`。",
            "重大决策记录在 `04-decisions/`。",
            "稳定事实和偏好保存在 `05-memory/`。",
            "周期复盘放入 `90-reviews/`。",
            "过期资料归档到 `99-archive/`。",
        ],
        "overview": "家庭总览",
        "updated": "更新时间：",
        "stage": "当前阶段",
        "snapshot": "家庭概况",
        "principles": "运行原则",
        "areas": "活跃领域",
        "projects": "活跃项目",
        "priorities": "当前优先级",
        "month": "本月家庭节奏",
        "month_label": "月份：",
        "focus": "本月重点",
        "calendar": "日程提醒",
        "money": "财务事项",
        "logistics": "家庭后勤",
        "review": "复盘记录",
        "risks_reminders": "风险与提醒",
        "risks": "风险",
        "reminders": "提醒",
        "watch": "观察清单",
        "facts": "家庭事实库",
        "facts_hint": "用简短、带日期的条目记录稳定事实。不确定的信息标记为“待确认”。",
        "values": "家庭价值观",
        "values_hint": "记录会长期影响家庭决策的原则、取舍和共识。",
        "preferences": "家庭偏好",
        "preferences_hint": "记录反复出现的家庭偏好、默认选择和边界。",
        "people": "重要人物与关系",
        "people_hint": "在注意隐私的前提下，记录重要人物和关系背景。",
    },
    "ja": {
        "workspace_title": "Family OS 家庭ワークスペース",
        "workspace_intro": "ここは非公開の家庭ワークスペースです。個人情報は Family OS スキル本体ではなく、ここに保存します。",
        "flow_title": "基本フロー",
        "flow": [
            "未整理の資料は `00-inbox/` に入れる。",
            "現在の優先事項は `01-dashboard/` に置く。",
            "継続的な領域は `02-areas/` に蓄積する。",
            "期限のある取り組みは `03-projects/` で管理する。",
            "重要な決定は `04-decisions/` に記録する。",
            "安定した事実と好みは `05-memory/` に保存する。",
            "定期レビューは `90-reviews/` に置く。",
            "古い資料は `99-archive/` に保管する。",
        ],
        "overview": "家庭の概要",
        "updated": "最終更新：",
        "stage": "現在の段階",
        "snapshot": "家庭スナップショット",
        "principles": "運用原則",
        "areas": "アクティブ領域",
        "projects": "アクティブプロジェクト",
        "priorities": "現在の優先事項",
        "month": "今月",
        "month_label": "月：",
        "focus": "重点",
        "calendar": "予定メモ",
        "money": "お金のメモ",
        "logistics": "家庭運営",
        "review": "レビューメモ",
        "risks_reminders": "リスクとリマインダー",
        "risks": "リスク",
        "reminders": "リマインダー",
        "watch": "ウォッチリスト",
        "facts": "家庭の事実",
        "facts_hint": "日付付きで短く記録します。不確かな情報は「要確認」とします。",
        "values": "家族の価値観",
        "values_hint": "意思決定を導く原則、トレードオフ、価値観を記録します。",
        "preferences": "好み",
        "preferences_hint": "繰り返し使う家庭の好みや既定値を記録します。",
        "people": "重要な人",
        "people_hint": "プライバシーに配慮して重要な人と関係性を記録します。",
    },
    "ko": {
        "workspace_title": "Family OS 가족 워크스페이스",
        "workspace_intro": "이곳은 비공개 가족 워크스페이스입니다. 개인 가족 정보는 Family OS 스킬 패키지가 아니라 이곳에 저장합니다.",
        "flow_title": "기본 흐름",
        "flow": [
            "원자료는 `00-inbox/`에 넣습니다.",
            "현재 우선순위는 `01-dashboard/`에 둡니다.",
            "장기 영역은 `02-areas/`에 쌓습니다.",
            "기간이 있는 일은 `03-projects/`에서 관리합니다.",
            "중요한 결정은 `04-decisions/`에 기록합니다.",
            "안정적인 사실과 선호는 `05-memory/`에 보관합니다.",
            "정기 리뷰는 `90-reviews/`에 둡니다.",
            "오래된 자료는 `99-archive/`에 보관합니다.",
        ],
        "overview": "가족 개요",
        "updated": "마지막 업데이트:",
        "stage": "현재 단계",
        "snapshot": "가족 현황",
        "principles": "운영 원칙",
        "areas": "활성 영역",
        "projects": "활성 프로젝트",
        "priorities": "현재 우선순위",
        "month": "이번 달",
        "month_label": "월:",
        "focus": "중점",
        "calendar": "일정 메모",
        "money": "재정 메모",
        "logistics": "가족 운영",
        "review": "리뷰 메모",
        "risks_reminders": "위험과 알림",
        "risks": "위험",
        "reminders": "알림",
        "watch": "관찰 목록",
        "facts": "가족 사실",
        "facts_hint": "짧은 날짜별 항목으로 기록합니다. 불확실한 정보는 `확인 필요`로 표시합니다.",
        "values": "가족 가치관",
        "values_hint": "결정을 이끄는 원칙, 절충, 가치관을 기록합니다.",
        "preferences": "선호",
        "preferences_hint": "반복되는 가족 선호와 기본값을 기록합니다.",
        "people": "중요한 사람들",
        "people_hint": "개인정보를 고려해 중요한 사람과 관계 맥락을 기록합니다.",
    },
    "es": {
        "workspace_title": "Espacio de Family OS",
        "workspace_intro": "Este es un espacio privado del hogar. Guarda la informacion familiar aqui, no en el paquete de la skill Family OS.",
        "flow_title": "Flujo principal",
        "flow": [
            "Pon el material sin procesar en `00-inbox/`.",
            "Mantén las prioridades actuales en `01-dashboard/`.",
            "Guarda los temas continuos en `02-areas/`.",
            "Gestiona los esfuerzos con fecha en `03-projects/`.",
            "Registra decisiones duraderas en `04-decisions/`.",
            "Conserva hechos y preferencias en `05-memory/`.",
            "Haz revisiones periodicas en `90-reviews/`.",
            "Archiva material antiguo en `99-archive/`.",
        ],
        "overview": "Resumen del hogar",
        "updated": "Ultima actualizacion:",
        "stage": "Etapa actual",
        "snapshot": "Situacion del hogar",
        "principles": "Principios de operacion",
        "areas": "Areas activas",
        "projects": "Proyectos activos",
        "priorities": "Prioridades actuales",
        "month": "Este mes",
        "month_label": "Mes:",
        "focus": "Foco",
        "calendar": "Notas de calendario",
        "money": "Notas financieras",
        "logistics": "Logistica familiar",
        "review": "Notas de revision",
        "risks_reminders": "Riesgos y recordatorios",
        "risks": "Riesgos",
        "reminders": "Recordatorios",
        "watch": "Lista de observacion",
        "facts": "Hechos del hogar",
        "facts_hint": "Usa entradas breves con fecha. Marca lo incierto como `por confirmar`.",
        "values": "Valores familiares",
        "values_hint": "Registra principios, compensaciones y valores que guian decisiones.",
        "preferences": "Preferencias",
        "preferences_hint": "Registra preferencias y valores predeterminados recurrentes.",
        "people": "Personas importantes",
        "people_hint": "Registra personas importantes y contexto relacional con cuidado de privacidad.",
    },
    "fr": {
        "workspace_title": "Espace Family OS",
        "workspace_intro": "Ceci est un espace familial prive. Conservez les informations du foyer ici, pas dans le paquet de competence Family OS.",
        "flow_title": "Flux principal",
        "flow": [
            "Placez les sources brutes dans `00-inbox/`.",
            "Gardez les priorites actuelles dans `01-dashboard/`.",
            "Stockez les domaines continus dans `02-areas/`.",
            "Suivez les efforts limites dans le temps dans `03-projects/`.",
            "Notez les decisions durables dans `04-decisions/`.",
            "Conservez les faits et preferences dans `05-memory/`.",
            "Faites les revues periodiques dans `90-reviews/`.",
            "Archivez l'ancien contenu dans `99-archive/`.",
        ],
        "overview": "Vue d'ensemble du foyer",
        "updated": "Derniere mise a jour :",
        "stage": "Etape actuelle",
        "snapshot": "Situation du foyer",
        "principles": "Principes de fonctionnement",
        "areas": "Domaines actifs",
        "projects": "Projets actifs",
        "priorities": "Priorites actuelles",
        "month": "Ce mois-ci",
        "month_label": "Mois :",
        "focus": "Priorite",
        "calendar": "Notes de calendrier",
        "money": "Notes financieres",
        "logistics": "Logistique familiale",
        "review": "Notes de revue",
        "risks_reminders": "Risques et rappels",
        "risks": "Risques",
        "reminders": "Rappels",
        "watch": "Points a surveiller",
        "facts": "Faits du foyer",
        "facts_hint": "Utilisez des entrees courtes datees. Marquez l'incertain comme `a confirmer`.",
        "values": "Valeurs familiales",
        "values_hint": "Notez les principes, arbitrages et valeurs qui guident les decisions.",
        "preferences": "Preferences",
        "preferences_hint": "Notez les preferences et reglages recurrents du foyer.",
        "people": "Personnes importantes",
        "people_hint": "Notez les personnes importantes avec attention a la confidentialite.",
    },
    "de": {
        "workspace_title": "Family OS Arbeitsbereich",
        "workspace_intro": "Dies ist ein privater Haushaltsarbeitsbereich. Speichere persoenliche Haushaltsinformationen hier, nicht im Family-OS-Skillpaket.",
        "flow_title": "Hauptablauf",
        "flow": [
            "Rohmaterial in `00-inbox/` ablegen.",
            "Aktuelle Prioritaeten in `01-dashboard/` pflegen.",
            "Dauerhafte Bereiche in `02-areas/` sammeln.",
            "Zeitlich begrenzte Vorhaben in `03-projects/` verfolgen.",
            "Dauerhafte Entscheidungen in `04-decisions/` dokumentieren.",
            "Stabile Fakten und Praeferenzen in `05-memory/` bewahren.",
            "Regelmaessige Reviews in `90-reviews/` ablegen.",
            "Altes Material in `99-archive/` archivieren.",
        ],
        "overview": "Haushaltsueberblick",
        "updated": "Zuletzt aktualisiert:",
        "stage": "Aktuelle Phase",
        "snapshot": "Haushaltssituation",
        "principles": "Betriebsprinzipien",
        "areas": "Aktive Bereiche",
        "projects": "Aktive Projekte",
        "priorities": "Aktuelle Prioritaeten",
        "month": "Dieser Monat",
        "month_label": "Monat:",
        "focus": "Fokus",
        "calendar": "Kalendernotizen",
        "money": "Finanznotizen",
        "logistics": "Familienlogistik",
        "review": "Review-Notizen",
        "risks_reminders": "Risiken und Erinnerungen",
        "risks": "Risiken",
        "reminders": "Erinnerungen",
        "watch": "Beobachtungsliste",
        "facts": "Haushaltsfakten",
        "facts_hint": "Nutze kurze datierte Eintraege. Markiere Unsicheres als `zu bestaetigen`.",
        "values": "Familienwerte",
        "values_hint": "Dokumentiere Prinzipien, Abwaegungen und Werte fuer Entscheidungen.",
        "preferences": "Praeferenzen",
        "preferences_hint": "Dokumentiere wiederkehrende Haushaltsvorlieben und Standards.",
        "people": "Wichtige Personen",
        "people_hint": "Dokumentiere wichtige Personen mit angemessener Privatsphaere.",
    },
    "pt": {
        "workspace_title": "Espaco Family OS",
        "workspace_intro": "Este e um espaco domestico privado. Guarde informacoes da familia aqui, nao no pacote da skill Family OS.",
        "flow_title": "Fluxo principal",
        "flow": [
            "Coloque material bruto em `00-inbox/`.",
            "Mantenha prioridades atuais em `01-dashboard/`.",
            "Guarde dominios continuos em `02-areas/`.",
            "Acompanhe esforcos com prazo em `03-projects/`.",
            "Registre decisoes duradouras em `04-decisions/`.",
            "Preserve fatos e preferencias em `05-memory/`.",
            "Faca revisoes periodicas em `90-reviews/`.",
            "Arquive material antigo em `99-archive/`.",
        ],
        "overview": "Visao geral da familia",
        "updated": "Ultima atualizacao:",
        "stage": "Fase atual",
        "snapshot": "Retrato da familia",
        "principles": "Principios de operacao",
        "areas": "Areas ativas",
        "projects": "Projetos ativos",
        "priorities": "Prioridades atuais",
        "month": "Este mes",
        "month_label": "Mes:",
        "focus": "Foco",
        "calendar": "Notas de calendario",
        "money": "Notas financeiras",
        "logistics": "Logistica familiar",
        "review": "Notas de revisao",
        "risks_reminders": "Riscos e lembretes",
        "risks": "Riscos",
        "reminders": "Lembretes",
        "watch": "Lista de observacao",
        "facts": "Fatos da familia",
        "facts_hint": "Use entradas curtas com data. Marque o incerto como `a confirmar`.",
        "values": "Valores familiares",
        "values_hint": "Registre principios, escolhas e valores que guiam decisoes.",
        "preferences": "Preferencias",
        "preferences_hint": "Registre preferencias e padroes recorrentes.",
        "people": "Pessoas importantes",
        "people_hint": "Registre pessoas importantes com cuidado de privacidade.",
    },
}


LANGUAGE_ALIASES = {
    "cn": "zh",
    "zh-cn": "zh",
    "zh-hans": "zh",
    "zh-hant": "zh",
    "zh-tw": "zh",
    "en-us": "en",
    "en-gb": "en",
    "ja-jp": "ja",
    "ko-kr": "ko",
    "es-es": "es",
    "es-mx": "es",
    "fr-fr": "fr",
    "de-de": "de",
    "pt-br": "pt",
    "pt-pt": "pt",
}


def normalize_language(language: str | None) -> str:
    raw = (language or "auto").strip()
    if not raw or raw.lower() == "auto":
        raw = (
            os.environ.get("FAMILY_OS_LANGUAGE")
            or os.environ.get("LC_ALL")
            or os.environ.get("LC_MESSAGES")
            or os.environ.get("LANG")
            or locale.getlocale()[0]
            or "en"
        )
    raw = raw.split(".", 1)[0].replace("_", "-").lower()
    if raw in LANGUAGE_ALIASES:
        return LANGUAGE_ALIASES[raw]
    base = raw.split("-", 1)[0]
    return base if base in TEXT else "en"


def read_config_language(config: Path) -> str | None:
    if not config.exists():
        return None
    for line in config.read_text(encoding="utf-8", errors="replace").splitlines():
        if line.strip().startswith("language:"):
            return line.split(":", 1)[1].strip() or None
    return None


def render_files(language: str) -> dict[str, str]:
    t = TEXT.get(normalize_language(language), TEXT["en"])
    flow = "\n".join(f"{idx}. {item}" for idx, item in enumerate(t["flow"], start=1))
    return {
        "README.md": f"""# {t["workspace_title"]}

{t["workspace_intro"]}

## {t["flow_title"]}

{flow}
""",
        "01-dashboard/household-overview.md": f"""# {t["overview"]}

{t["updated"]}

## {t["stage"]}

## {t["snapshot"]}

## {t["principles"]}

## {t["areas"]}

## {t["projects"]}
""",
        "01-dashboard/current-priorities.md": f"""# {t["priorities"]}

{t["updated"]}

## Now

## Next

## Waiting
""",
        "01-dashboard/this-month.md": f"""# {t["month"]}

{t["month_label"]}

## {t["focus"]}

## {t["calendar"]}

## {t["money"]}

## {t["logistics"]}

## {t["review"]}
""",
        "01-dashboard/risks-and-reminders.md": f"""# {t["risks_reminders"]}

{t["updated"]}

## {t["risks"]}

## {t["reminders"]}

## {t["watch"]}
""",
        "05-memory/household-facts.md": f"""# {t["facts"]}

{t["facts_hint"]}
""",
        "05-memory/family-values.md": f"""# {t["values"]}

{t["values_hint"]}
""",
        "05-memory/preferences.md": f"""# {t["preferences"]}

{t["preferences_hint"]}
""",
        "05-memory/important-people.md": f"""# {t["people"]}

{t["people_hint"]}
""",
    }


def write_if_missing(path: Path, content: str) -> bool:
    if path.exists():
        return False
    path.parent.mkdir(parents=True, exist_ok=True)
    path.write_text(content, encoding="utf-8")
    return True


def archive_existing_workspace(workspace: Path) -> Path | None:
    if not workspace.exists() or not any(workspace.iterdir()):
        return None

    archive_root = workspace / "99-archive"
    archive_root.mkdir(parents=True, exist_ok=True)
    stamp = datetime.now().strftime("%Y%m%d-%H%M%S")
    archive_dir = archive_root / f"legacy-import-{stamp}"
    archive_dir.mkdir()

    for item in list(workspace.iterdir()):
        if item.name == "99-archive":
            continue
        shutil.move(str(item), str(archive_dir / item.name))

    previous_archive = archive_dir / "previous-99-archive"
    previous_archive.mkdir()
    for item in list(archive_root.iterdir()):
        if item.name == archive_dir.name:
            continue
        shutil.move(str(item), str(previous_archive / item.name))

    if not any(previous_archive.iterdir()):
        previous_archive.rmdir()

    return archive_dir


def write_config(config: Path, workspace: Path, language: str, ask_sensitive: bool) -> None:
    config.parent.mkdir(parents=True, exist_ok=True)
    text = f"""workspace: {workspace}
language: {language}
privacy_mode: local-only
auto_update:
  enabled: true
  update_dashboard: true
  update_memory: true
  update_projects: true
  ask_before_sensitive_write: {str(ask_sensitive).lower()}
"""
    config.write_text(text, encoding="utf-8")


def init_workspace(workspace: Path, archive_existing: bool, language: str) -> tuple[list[str], Path | None]:
    workspace.mkdir(parents=True, exist_ok=True)
    archive_dir = archive_existing_workspace(workspace) if archive_existing else None

    created: list[str] = []
    for directory in DIRS:
        path = workspace / directory
        if not path.exists():
            path.mkdir(parents=True)
            created.append(directory + "/")

    for rel, content in render_files(language).items():
        if write_if_missing(workspace / rel, content):
            created.append(rel)

    return created, archive_dir


def main() -> int:
    parser = argparse.ArgumentParser(description="Initialize a Family OS workspace.")
    parser.add_argument("--workspace", default=os.environ.get("FAMILY_OS_HOME", str(DEFAULT_WORKSPACE)))
    parser.add_argument("--config", default=str(DEFAULT_CONFIG))
    parser.add_argument("--language", default="auto", help="Template language, e.g. auto, zh-CN, en-US, ja, ko, es, fr, de, pt.")
    parser.add_argument("--archive-existing", action="store_true")
    parser.add_argument("--ask-before-sensitive-write", action=argparse.BooleanOptionalAction, default=True)
    args = parser.parse_args()

    workspace = Path(args.workspace).expanduser().resolve()
    config = Path(args.config).expanduser().resolve()

    requested_language = args.language
    if requested_language.strip().lower() == "auto":
        requested_language = read_config_language(config) or requested_language
    language = normalize_language(requested_language)
    created, archive_dir = init_workspace(workspace, args.archive_existing, language)
    write_config(config, workspace, language, args.ask_before_sensitive_write)

    print(f"workspace: {workspace}")
    print(f"config: {config}")
    print(f"language: {language}")
    if archive_dir:
        print(f"legacy_archive: {archive_dir}")
    print(f"created: {len(created)}")
    for rel in created:
        print(f"  - {rel}")
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
