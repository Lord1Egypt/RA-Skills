#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
User Onboarding Module for Four-Dimensional Deep Reading
Version: 1.7.1

Provides language-specific onboarding messages for first-time users.
"""

from typing import Dict, Optional


# English Onboarding
ENGLISH_ONBOARDING = """
🎓 Welcome to Four-Dimensional Deep Reading!

This skill summons 4 virtual personas to analyze your content from different angles simultaneously:

┌─────────────────────────────────────────────────────────────┐
│  🔬 Axiom Analyst        →  First Principles Thinking        │
│     Strips away surface details to find fundamental truths  │
│                                                             │
│  📝 LMS Architect        →  Structured Notes                │
│     Organizes insights into Logic-Method-Summary format     │
│                                                             │
│  ⚡ Black Swan Hunter    →  Counterarguments & Edge Cases   │
│     Finds what could go wrong and challenges assumptions    │
│                                                             │
│  🎲 Random Variable X    →  Unexpected Perspectives         │
│     Brings fresh insights from random identity angles       │
└─────────────────────────────────────────────────────────────┘

📊 What you'll get:
• A comprehensive analysis report (saved to workspace/reports/)
• Multiple perspectives on the same content
• Actionable insights and structured notes
• Critical thinking challenges

💡 Tips for best results:
• Provide specific book titles or upload files for deeper analysis
• Ask follow-up questions about specific sections
• Use the LMS structure to create your own notes

Ready to start? Just provide a book title or file!
"""

# Chinese Onboarding
CHINESE_ONBOARDING = """
🎓 欢迎使用四维深度阅读！

本技能召唤 4 个虚拟角色从不同角度同时分析你的内容：

┌─────────────────────────────────────────────────────────────┐
│  🔬 第一性原理师        →  公理化思维分析                    │
│     剥离表象，追溯底层假设和核心公理                        │
│                                                             │
│  📝 结构化笔记官        →  LMS 结构输出                     │
│     将洞察组织为 Logic-Method-Summary 格式                  │
│                                                             │
│  ⚡ 黑天鹅猎手          →  反驳论证与边界检测                │
│     寻找失效点和边缘情况，挑战假设                          │
│                                                             │
│  🎲 随机变量 X          →  意外视角洞察                      │
│     从随机身份角度带来全新思考                              │
└─────────────────────────────────────────────────────────────┘

📊 你将获得：
• 一份综合分析报告（自动保存到 workspace/reports/）
• 同一内容的多视角解读
• 可执行的洞察和结构化笔记
• 批判性思维挑战

💡 使用建议：
• 提供具体书名或上传文件可获得更深入的分析
• 对特定部分提出追问
• 使用 LMS 结构创建自己的笔记

准备好了吗？提供一本书名或文件即可开始！
"""

# Japanese Onboarding
JAPANESE_ONBOARDING = """
🎓 四次元深読みへようこそ！

このスキルは4人の仮想ペルソナを召喚し、異なる角度から同時にコンテンツを分析します：

┌─────────────────────────────────────────────────────────────┐
│  🔬 公理分析者          →  第一原理思考                      │
│     表面を取り除き、根本的な真実を見つける                  │
│                                                             │
│  📝 LMS設計者           →  構造化ノート                      │
│     洞察をLogic-Method-Summary形式で整理                    │
│                                                             │
│  ⚡ ブラックスワン探求者 →  反論とエッジケース               │
│     何がうまくいかないかを見つけ、仮定に挑戦                │
│                                                             │
│  🎲 ランダム変数X       →  予期しない視点                    │
│     ランダムなアイデンティティから新鮮な洞察をもたらす      │
└─────────────────────────────────────────────────────────────┘

📊 得られるもの：
• 包括的な分析レポート（workspace/reports/に保存）
• 同じコンテンツの複数の視点
• 実行可能な洞察と構造化されたノート
• 批判的思考の課題

💡 最高の結果を得るためのヒント：
• より深い分析のために具体的な書名を提供するか、ファイルをアップロード
• 特定のセクションについてフォローアップの質問をする
• LMS構造を使用して自分のノートを作成

準備はできましたか？書名またはファイルを提供してください！
"""

# Korean Onboarding
KOREAN_ONBOARDING = """
🎓 4차원 깊은 읽기에 오신 것을 환영합니다!

이 스킬은 4명의 가상 페르소나를 소환하여 다른 각도에서 동시에 콘텐츠를 분석합니다:

┌─────────────────────────────────────────────────────────────┐
│  🔬 공리 분석가         →  제1원칙 사고                      │
│     표면을 벗겨내고 근본적인 진실을 찾습니다                │
│                                                             │
│  📝 LMS 설계자          →  구조화된 노트                     │
│     통찰력을 Logic-Method-Summary 형식으로 정리             │
│                                                             │
│  ⚡ 블랙 스완 사냥꾼     →  반론과 엣지 케이스               │
│     무엇이 잘못될 수 있는지 찾고 가정에 도전                │
│                                                             │
│  🎲 무작위 변수 X       →  예상치 못한 관점                  │
│     무작위 정체성에서 새로운 통찰을 가져옵니다              │
└─────────────────────────────────────────────────────────────┘

📊 얻을 수 있는 것:
• 포괄적인 분석 보고서 (workspace/reports/에 저장)
• 동일한 콘텐츠에 대한 여러 관점
• 실행 가능한 통찰력과 구조화된 노트
• 비판적 사고 과제

💡 최상의 결과를 위한 팁:
• 더 깊은 분석을 위해 구체적인 책 제목을 제공하거나 파일을 업로드
• 특정 섹션에 대한 후속 질문
• LMS 구조를 사용하여 자신만의 노트 만들기

준비되셨나요? 책 제목이나 파일을 제공하세요!
"""

# French Onboarding
FRENCH_ONBOARDING = """
🎓 Bienvenue dans la Lecture Profonde Quadridimensionnelle!

Cette compétence invoque 4 personas virtuels pour analyser votre contenu sous différents angles simultanément:

┌─────────────────────────────────────────────────────────────┐
│  🔬 Analyste d'Axiomes  →  Pensée des Premiers Principes    │
│     Élimine les détails de surface pour trouver les vérités │
│                                                             │
│  📝 Architecte LMS      →  Notes Structurées                │
│     Organise les insights en format Logic-Method-Summary    │
│                                                             │
│  ⚡ Chasseur de Cygne Noir →  Contre-arguments et Cas Limites│
│     Trouve ce qui pourrait mal tourner et défie les hypothèses│
│                                                             │
│  🎲 Variable Aléatoire X →  Perspectives Inattendues        │
│     Apporte des insights frais d'angles identitaires aléatoires│
└─────────────────────────────────────────────────────────────┘

📊 Ce que vous obtiendrez:
• Un rapport d'analyse complet (sauvegardé dans workspace/reports/)
• Plusieurs perspectives sur le même contenu
• Des insights actionnables et des notes structurées
• Des défis de pensée critique

💡 Conseils pour de meilleurs résultats:
• Fournissez des titres de livres spécifiques ou téléchargez des fichiers
• Posez des questions de suivi sur des sections spécifiques
• Utilisez la structure LMS pour créer vos propres notes

Prêt à commencer? Fournissez simplement un titre de livre ou un fichier!
"""

# German Onboarding
GERMAN_ONBOARDING = """
🎓 Willkommen beim Vierdimensionalen Tiefenlesen!

Diese Fähigkeit beschwört 4 virtuelle Personas, um Ihren Inhalt gleichzeitig aus verschiedenen Blickwinkeln zu analysieren:

┌─────────────────────────────────────────────────────────────┐
│  🔬 Axiom-Analytiker    →  First-Principles-Denken          │
│     Entfernt Oberflächliches, um fundamentale Wahrheiten zu finden│
│                                                             │
│  📝 LMS-Architekt       →  Strukturierte Notizen            │
│     Organisiert Erkenntnisse im Logic-Method-Summary-Format │
│                                                             │
│  ⚡ Schwarzer-Schwan-Jäger →  Gegenargumente & Randfälle   │
│     Findet was schiefgehen könnte und stellt Annahmen in Frage│
│                                                             │
│  🎲 Zufallsvariable X   →  Unerwartete Perspektiven          │
│     Bringt frische Einblicke aus zufälligen Identitätswinkeln│
└─────────────────────────────────────────────────────────────┘

📊 Was Sie erhalten:
• Einen umfassenden Analysebericht (gespeichert in workspace/reports/)
• Mehrere Perspektiven auf denselben Inhalt
• Umsetzbare Erkenntnisse und strukturierte Notizen
• Kritisches Denken Herausforderungen

💡 Tipps für beste Ergebnisse:
• Geben Sie spezifische Buchtitel an oder laden Sie Dateien hoch
• Stellen Sie Folgefragen zu bestimmten Abschnitten
• Verwenden Sie die LMS-Struktur für eigene Notizen

Bereit anzufangen? Geben Sie einfach einen Buchtitel oder eine Datei an!
"""

# Spanish Onboarding
SPANISH_ONBOARDING = """
🎓 ¡Bienvenido a la Lectura Profunda Cuatridimensional!

Esta habilidad invoca 4 personas virtuales para analizar tu contenido desde diferentes ángulos simultáneamente:

┌─────────────────────────────────────────────────────────────┐
│  🔬 Analista de Axiomas →  Pensamiento de Primeros Principios│
│     Elimina detalles superficiales para encontrar verdades  │
│                                                             │
│  📝 Arquitecto LMS      →  Notas Estructuradas              │
│     Organiza ideas en formato Logic-Method-Summary          │
│                                                             │
│  ⚡ Cazador de Cisne Negro →  Contraargumentos y Casos Límite│
│     Encuentra qué podría salir mal y desafía suposiciones   │
│                                                             │
│  🎲 Variable Aleatoria X →  Perspectivas Inesperadas        │
│     Trae insights frescos desde ángulos de identidad aleatorios│
└─────────────────────────────────────────────────────────────┘

📊 Lo que obtendrás:
• Un informe de análisis completo (guardado en workspace/reports/)
• Múltiples perspectivas sobre el mismo contenido
• Insights accionables y notas estructuradas
• Desafíos de pensamiento crítico

💡 Consejos para mejores resultados:
• Proporciona títulos de libros específicos o sube archivos
• Haz preguntas de seguimiento sobre secciones específicas
• Usa la estructura LMS para crear tus propias notas

¿Listo para empezar? ¡Solo proporciona un título de libro o archivo!
"""

# Portuguese Onboarding
PORTUGUESE_ONBOARDING = """
🎓 Bem-vindo à Leitura Profunda Quadridimensional!

Esta habilidade invoca 4 personas virtuais para analisar seu conteúdo de diferentes ângulos simultaneamente:

┌─────────────────────────────────────────────────────────────┐
│  🔬 Analista de Axiomas →  Pensamento de Primeiros Princípios│
│     Remove detalhes superficiais para encontrar verdades    │
│                                                             │
│  📝 Arquiteto LMS       →  Notas Estruturadas               │
│     Organiza insights em formato Logic-Method-Summary       │
│                                                             │
│  ⚡ Caçador de Cisne Negro →  Contra-argumentos e Casos Limite│
│     Encontra o que pode dar errado e desafia suposições     │
│                                                             │
│  🎲 Variável Aleatória X →  Perspectivas Inesperadas        │
│     Traz insights frescos de ângulos de identidade aleatórios│
└─────────────────────────────────────────────────────────────┘

📊 O que você obterá:
• Um relatório de análise completo (salvo em workspace/reports/)
• Múltiplas perspectivas sobre o mesmo conteúdo
• Insights acionáveis e notas estruturadas
• Desafios de pensamento crítico

💡 Dicas para melhores resultados:
• Forneça títulos de livros específicos ou carregue arquivos
• Faça perguntas de acompanhamento sobre seções específicas
• Use a estrutura LMS para criar suas próprias notas

Pronto para começar? Basta fornecer um título de livro ou arquivo!
"""

# Russian Onboarding
RUSSIAN_ONBOARDING = """
🎓 Добро пожаловать в Четырёхмерное Глубокое Чтение!

Этот навык призывает 4 виртуальных персоны для анализа вашего контента с разных углов одновременно:

┌─────────────────────────────────────────────────────────────┐
│  🔬 Аналитик Аксиом     →  Мышление Первых Принципов        │
│     Убирает поверхностные детали, чтобы найти истину        │
│                                                             │
│  📝 Архитектор LMS      →  Структурированные Заметки        │
│     Организует идеи в формате Logic-Method-Summary          │
│                                                             │
│  ⚡ Охотник за Чёрным Лебедем →  Контраргументы и Краевые Случаи│
│     Находит что может пойти не так и оспаривает предположения│
│                                                             │
│  🎲 Случайная Переменная X →  Неожиданные Перспективы       │
│     Приносит свежие идеи со случайных углов идентичности    │
└─────────────────────────────────────────────────────────────┘

📊 Что вы получите:
• Комплексный аналитический отчёт (сохранён в workspace/reports/)
• Множество перспектив на один и тот же контент
• Практические идеи и структурированные заметки
• Задачи критического мышления

💡 Советы для лучших результатов:
• Предоставьте конкретные названия книг или загрузите файлы
• Задавайте уточняющие вопросы по конкретным разделам
• Используйте структуру LMS для создания собственных заметок

Готовы начать? Просто предоставьте название книги или файл!
"""


# Language to onboarding mapping
ONBOARDING_TEMPLATES: Dict[str, str] = {
    "en": ENGLISH_ONBOARDING,
    "zh": CHINESE_ONBOARDING,
    "ja": JAPANESE_ONBOARDING,
    "ko": KOREAN_ONBOARDING,
    "fr": FRENCH_ONBOARDING,
    "de": GERMAN_ONBOARDING,
    "es": SPANISH_ONBOARDING,
    "pt": PORTUGUESE_ONBOARDING,
    "ru": RUSSIAN_ONBOARDING,
}


def get_onboarding_message(language: str) -> str:
    """
    Get language-specific onboarding message.
    
    Args:
        language: Language code (en, zh, ja, ko, fr, de, es, pt, ru)
        
    Returns:
        Onboarding message in the specified language (fallback to English)
    """
    return ONBOARDING_TEMPLATES.get(language, ONBOARDING_TEMPLATES["en"])


def should_show_onboarding(user_id: str, skill_usage_count: Dict[str, int]) -> bool:
    """
    Determine if onboarding should be shown to the user.
    
    Args:
        user_id: Unique identifier for the user
        skill_usage_count: Dictionary tracking usage count per user
        
    Returns:
        True if onboarding should be shown, False otherwise
    """
    return skill_usage_count.get(user_id, 0) < 1


def get_supported_languages() -> list:
    """Get list of supported languages for onboarding."""
    return list(ONBOARDING_TEMPLATES.keys())


if __name__ == "__main__":
    # Demo: Print all onboarding messages
    print("=" * 60)
    print("Four-Dimensional Deep Reading - Onboarding Templates")
    print("=" * 60)
    print(f"\nSupported languages: {', '.join(get_supported_languages())}")
    print("\n" + "=" * 60)
    
    for lang in get_supported_languages():
        print(f"\n{'=' * 60}")
        print(f"Language: {lang.upper()}")
        print("=" * 60)
        print(get_onboarding_message(lang))
