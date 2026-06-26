# calibre-ebooks

Skill OpenClaw para consultar e operar uma biblioteca Calibre local por meio de
uma API Books local e scripts auxiliares.

Este projeto trabalha somente com livros que já existem na biblioteca Calibre
configurada. Ele não baixa, procura ou adiciona livros de fontes externas.

## Componentes

- `SKILL.md`: fluxo recomendado para agentes OpenClaw.
- `scripts/books_api_client.py`: cliente Python para consultar a API local.
- `calibre-openclaw-server/`: servidor FastAPI, RAG semântico e serviços systemd.
- `.env`: configuração local usada pelos scripts e pelo servidor.

## API Local

Com o servidor ativo:

- Swagger: `http://127.0.0.1:6180/docs`
- ReDoc: `http://127.0.0.1:6180/redoc`
- OpenAPI: `http://127.0.0.1:6180/openapi.json`

## Uso Rápido

```bash
python3 skills/calibre-ebooks/scripts/books_api_client.py docs
python3 skills/calibre-ebooks/scripts/books_api_client.py paths
python3 skills/calibre-ebooks/scripts/books_api_client.py search "termo" --limit 10
python3 skills/calibre-ebooks/scripts/books_api_client.py book 123
python3 skills/calibre-ebooks/scripts/books_api_client.py request GET /books --query q=python
```

## Configuração

Crie ou atualize `skills/calibre-ebooks/.env` com:

- `BOOKS_API_URL`
- `CALIBRE_DB_PATH`
- `CALIBRE_LIBRARY_PATH`
- `API_KEY`
- `POSTGRESQL_DB_USER`
- `POSTGRESQL_DB_PASSWD`
- `POSTGRESQL_DB_DATABASE`
- `POSTGRESQL_DB_HOST`
- `POSTGRESQL_DB_PORT`

As configurações completas ficam documentadas em `.env.example` e no README do
servidor em `calibre-openclaw-server/`.

Recursos que expõem conteúdo completo, enumeram rede local, fazem auto-sync por
GET, usam Ollama remoto ou executam RAG em segundo plano exigem opt-in explícito
no `.env`.

## RAG

O RAG semântico é executado pelo servidor. Para ativar processamento contínuo
manual:

```bash
cd skills/calibre-ebooks
./calibre-openclaw-server/run-rag.sh
```

Para instalação, serviço systemd e agendamento noturno, consulte:

```text
skills/calibre-ebooks/calibre-openclaw-server/README.md
```
