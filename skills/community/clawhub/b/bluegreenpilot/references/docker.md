# Docker and Mixed Docker Deployments

Use this reference when any environment deploys with Docker.

## Discovery

Look for:

- `Dockerfile`
- `docker-compose.yml`, `compose.yml`
- image registry config
- CI build/push workflow
- environment-specific compose files
- exposed ports and healthchecks

## Safe Flow

1. Build or pull image for the candidate release.
2. Deploy candidate image to inactive slot.
3. Verify container health.
4. Verify application healthcheck URL.
5. Run smoke commands.
6. Confirm switch method.
7. Switch traffic only after approval.

## Mixed Mode

If homolog uses Docker but prod does not, do not assume parity. Treat homolog as
a rehearsal for application behavior, not proof of production deploy mechanics.

If prod uses Docker but homolog does not, ask why. Recommend adding a Docker
homolog path or clearly documenting the divergence.

## Docker Checks

Use only commands relevant to the project:

```bash
docker compose ps
docker compose logs --no-color --tail=100
docker image ls
docker inspect <container>
```

Do not remove containers, volumes, or images unless the user explicitly approves.

