# Stack conventions: Java, Python and the database service

For Node.js projects see the [example project](example-nextjs-sqlite/). Other stacks are made ready as described here; the general requirements (listen on `0.0.0.0:$PORT`, a health check endpoint, a read-only root filesystem, `USER 10001`, declared storage) do not change. Base image names and the runtime constraints are in [base images](base-images.md).

## The database service (MySQL / PostgreSQL)

When a project uses MySQL or PostgreSQL, do not put the database into the application's image and do not connect to a database on the development machine: declare it in the manifest and the platform provides the database.

~~~json
"database": { "type": "mysql", "version": "8.4" }
~~~

- type / version: `mysql` 8.4, `postgres` 17: the platform offers one stable version of each, and `version` may be left out. A project developed against MySQL 8.0 or PostgreSQL 15 / 16 usually runs on these unchanged; do not ask for another version.
- mode:
  - `shared` (the default; nothing needs to be written): the platform creates a database and an account for the project inside a shared database instance. The account can reach only its own database, which keeps it logically apart from other projects. Right for most projects, and economical.
  - `dedicated`: the project has a database container of its own, and `memory` can set its memory (default 512m, at least 256m). For projects with much data, heavy load or strict isolation needs. memory cannot be written with shared mode.
  - Use shared unless the user asks otherwise. When dedicated is needed, give the user the reason and get their confirmation.
  - Whether it can be used at all is decided by the user's plan (`limits.database` in `appcli plan --json`): with `none` there is no database service, with `shared` dedicated cannot be used. Beyond the plan, the deployment returns `PLAN_LIMIT_EXCEEDED`.
- The database can be reached only on the project's internal network (host name `db`); no port is open to the outside. Its data is kept for good: deployments, rollbacks and restarts do not lose it.
- The connection details are injected into the application by the platform. Do not declare these names in env, and do not write the database name, user name or password into code or configuration files:

  | Variable | MySQL | PostgreSQL |
  |---|---|---|
  | `DATABASE_URL` | `mysql://<user>:<password>@db:3306/<database>` | `postgresql://<user>:<password>@db:5432/<database>` |
  | `JDBC_DATABASE_URL` | `jdbc:mysql://db:3306/<database>` | `jdbc:postgresql://db:5432/<database>` |
  | `DB_HOST` `DB_PORT` `DB_NAME` `DB_USER` `DB_PASSWORD` | `db` `3306` `<database>` `<user>` `<password>` | `db` `5432` `<database>` `<user>` `<password>` |

  The database name and the user name are assigned by the platform (different for every project with shared, `app` with dedicated); the code must read them from the variables.

- The application's account has rights only inside its own database: it cannot create databases, reach other databases, or use anything that needs administrator rights (MySQL's SUPER and FILE; PostgreSQL's superuser and untrusted extensions). PostgreSQL can use trusted extensions only (such as pgcrypto, uuid-ossp, hstore, citext).
- The character set is utf8mb4 by default (for MySQL the server, the database and the application's connection are all utf8mb4, with collation utf8mb4_0900_ai_ci; PostgreSQL is UTF8). Chinese and emoji need no further configuration; table definitions should not name another character set such as latin1 or utf8mb3.
- The schema is created by the application's migration tool at start (Flyway, Liquibase, Prisma migrate, Alembic, Django migrate and so on). The application is started only once the database is ready.
- After the project's first successful deployment the database's type, version or mode can no longer be changed, and the database cannot be removed (`DATABASE_CHANGE_NOT_ALLOWED`); when that is needed the administrator handles it. A rollback to an older version with different database settings is not possible.
- The pre-deployment backup (backupBeforeDeploy) is a SQL dump of the database. `appcli restore` replaces the whole content of the database with it; the data from before the replacement is saved automatically as a "pre-restore" backup.
- Migrating local data (first deployment, with the user's agreement): ask the user to export a SQL file on their own computer and put it into the project, write `"localPath": "db-dump.sql"` in the manifest, and deploy with `--import-data`. Add the dump file to .gitignore and .dockerignore.
  - MySQL: `mysqldump --single-transaction --no-tablespaces --set-gtid-purged=OFF <database> > db-dump.sql`
  - PostgreSQL: `pg_dump --no-owner --no-privileges <database> > db-dump.sql`
  - The dump is loaded into the project's own database as the project's account: it must not contain statements that switch databases, such as `CREATE DATABASE`, `USE` or `\connect`, nor statements that need administrator rights. The DEFINER of views, triggers and stored procedures is changed to the project's account.
- Local development keeps its configuration: where the code reads the variables above, the value it used locally is the default.

## Java (Spring Boot)

~~~dockerfile
FROM maven-3.9-java-21 AS build
WORKDIR /src
COPY .mvn/settings.xml /root/.m2/settings.xml
COPY pom.xml .
RUN mvn -B -q dependency:go-offline
COPY src ./src
RUN mvn -B -q package -DskipTests

FROM java-21-jre
WORKDIR /app
COPY --from=build /src/target/*.jar /app/app.jar
ENV JAVA_TOOL_OPTIONS="-XX:MaxRAMPercentage=75 -Djava.io.tmpdir=/tmp"
USER 10001
CMD ["java", "-jar", "/app/app.jar"]
~~~

- Maven dependencies come from Alibaba Cloud: `.mvn/settings.xml` in the project configures the mirror `https://maven.aliyun.com/repository/public` (`mirrorOf` is `*`). Gradle builds with `gradle-8-java-21`; in `settings.gradle`, put the Alibaba Cloud repository first in both `pluginManagement` and `dependencyResolutionManagement`.
- `application.properties`: `server.port=${PORT:8080}`; with the database service, `spring.datasource.url=${JDBC_DATABASE_URL:<the local value>}`, `spring.datasource.username=${DB_USER:<the local value>}`, `spring.datasource.password=${DB_PASSWORD:<the local value>}`.
- Health check: with Actuator, healthcheckPath is `/actuator/health`; otherwise add a simple endpoint that answers 200. Neither may be blocked by Spring Security.
- The JVM version follows the project's `java.version` / `release` setting: 17 or 21. containerPort is the default of `server.port` (usually 8080). For resources.memory at least 512m is advisable.
- The application writes files only to declared storage or to `/tmp`; the upload directory is read from `UPLOAD_DIR`.

## Java (WAR + Tomcat)

Use `tomcat-10.1-java-21` (Jakarta EE 10; an old javax.* project needs Tomcat 9, which the administrator has to provide when the platform does not offer it). Tomcat writes into its own installation directory by default; under a read-only root filesystem its working directories have to move under `/app`:

~~~dockerfile
FROM tomcat-10.1-java-21
ENV CATALINA_BASE=/app/tomcat
RUN mkdir -p /app/tomcat/webapps && cp -r /usr/local/tomcat/conf /app/tomcat/conf
COPY target/app.war /app/tomcat/webapps/ROOT.war
USER 10001
~~~

In the manifest declare `/app/tomcat/logs`, `/app/tomcat/temp` and `/app/tomcat/work` as ephemeral storage. When the WAR has to be unpacked, unpack it in the build stage into `/app/tomcat/webapps/ROOT/` (webapps is read-only at run time).

## Python

~~~dockerfile
FROM python-3.12 AS runtime
WORKDIR /app
ENV PYTHONDONTWRITEBYTECODE=1 PYTHONUNBUFFERED=1 PIP_INDEX_URL=https://mirrors.aliyun.com/pypi/simple/
COPY requirements.txt .
RUN pip install --no-cache-dir -r requirements.txt
COPY . .
USER 10001
CMD ["sh", "-c", "gunicorn -b 0.0.0.0:${PORT} app:app"]
~~~

- pip uses the Alibaba Cloud mirror (`PIP_INDEX_URL`). Dependencies that have to be compiled get `gcc` and the like in a build stage (switch the apt source first, see base images), with only the installed result copied into the runtime stage; or use prebuilt manylinux wheels.
- Connecting to MySQL 8.x: PyMySQL also needs `cryptography` installed (MySQL 8's default caching_sha2_password authentication needs it; without it the connection fails with `'cryptography' package is required`). mysqlclient does not.
- Serve with a production server (gunicorn, uvicorn) listening on `0.0.0.0:$PORT`, not with the framework's development server.
- Django: `ALLOWED_HOSTS` includes the host of the application's address; `DATABASES` reads `DATABASE_URL` with `dj-database-url`; static files are collected in the build stage with `collectstatic` and served by WhiteNoise; `python manage.py migrate` runs first in the start command.
- Under a read-only root filesystem Python cannot write `__pycache__` (turned off with `PYTHONDONTWRITEBYTECODE=1`); caches and temporary files go to `/tmp` or to declared storage.
