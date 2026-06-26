# Odontosoft Skill

Skill para OpenClaw que permite gestionar turnos odontológicos a través de la API REST de Odontosoft.

## Qué hace

| Herramienta | Descripción |
|---|---|
| `get_doctores` | Lista los odontólogos activos de la clínica |
| `get_turnos_disponibles` | Muestra los horarios libres de un doctor en una fecha |
| `buscar_paciente` | Busca un paciente por número de documento |
| `agendar_turno` | Crea un nuevo turno (valida disponibilidad antes) |

## Instalación

```
/skills install @odontosoft/odontosoft
```

## Configuración requerida

En `openclaw.json`:

```json
{
  "skills": {
    "@odontosoft/odontosoft": {
      "enabled": true,
      "config": {
        "baseUrl": "${ODONTOSOFT_BASE_URL}",
        "apiKey":  "${ODONTOSOFT_TOKEN}"
      }
    }
  }
}
```

Configurar las variables de entorno:

```
/secrets set ODONTOSOFT_BASE_URL https://api.odontosoft.com.py
/secrets set ODONTOSOFT_TOKEN    tu_token_aqui
```

## Ejemplos de uso

> "Mostrá los doctores disponibles"

> "Qué turnos tiene el doctor 2 para el 25 de marzo?"

> "Buscá al paciente con DNI 12345678"

> "Agendá un turno para el paciente 5 con el doctor 1 el 2026-03-25 a las 09:00 por consulta general"

## Permisos

Este skill solo hace peticiones a `api.odontosoft.com.py`. No accede al sistema de archivos ni a otros servicios.

## Tests

```bash
node --experimental-vm-modules test/index.test.js
```
