Пример использования скила

1) Установить локально (если опубликован):

   clawhub install clawhub-intro-skill

2) Опубликовать скила (в корне папки скила):

   clawhub publish ./ --slug clawhub-intro-skill --name "ClawHub Intro Skill" --version 0.1.0 --tags latest

3) Обновить установленный скилл:

   clawhub update clawhub-intro-skill

4) Синхронизировать несколько скилов:

   clawhub sync --all
