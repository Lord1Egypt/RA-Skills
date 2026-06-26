# 📅 argentina-fiscal-calendar

> Calendario fiscal argentino completo para OpenClaw — ARCA (ex AFIP)

Skill gratuito para [OpenClaw](https://openclaw.ai) que convierte a tu agente en un asistente fiscal para PyMEs argentinas. Cubre todas las obligaciones recurrentes ante ARCA con reglas de vencimiento, traslado por feriados, recategorizaciones y fechas especiales 2026.

**Sin APIs externas. Sin credenciales. Funciona offline.**

---

## ¿Qué hace?

- Responde preguntas sobre vencimientos fiscales en lenguaje natural
- Calcula automáticamente el traslado por feriados y fines de semana
- Filtra por terminación de CUIT y régimen (monotributo, autónomos, RI, empleador)
- Envía alertas proactivas los lunes con los vencimientos de la semana (heartbeat)
- Avisa sobre recategorizaciones del Monotributo antes de que venzan

## Obligaciones cubiertas

| Régimen | Cobertura |
|---------|-----------|
| Monotributo | Pago mensual, recategorización semestral, actualización de valores |
| Autónomos (RGSS) | Pago mensual por terminación CUIT, recategorización anual |
| IVA (RI) | DDJJ mensual + Libro IVA Digital por terminación CUIT |
| Ganancias | Anticipos mensuales, DDJJ anual (personas físicas y jurídicas) |
| Bienes Personales | DDJJ anual período fiscal 2025 |
| SUSS / F.931 | Empleadores — aportes y contribuciones mensuales |
| Servicio doméstico | F.102/RT y F.575/RT |
| SIRADIG / F.572 | Relación de dependencia — vencimiento anual 31/03 |

## Instalación

```bash
clawhub install argentina-fiscal-calendar
```

O clonar manualmente en tu directorio de skills:

```bash
git clone https://github.com/centriqs-ai/skills.git
cp -r skills/argentina-fiscal-calendar ~/.openclaw/skills/
```

## Uso

```
fiscal hoy          # Vencimientos de hoy
fiscal semana       # Próximos 7 días
fiscal mes          # Todo el mes en curso
fiscal mes junio    # Mes específico
fiscal categoria monotributo
fiscal recategorizacion
fiscal feriados
```

## Configuración (opcional)

Al instalar, completar `~/centriqs/fiscal/config.md` con tu terminación de CUIT y régimen para recibir alertas personalizadas:

```markdown
cuit_terminacion: 03
regimen: responsable_inscripto
empleador: si
anticipacion_alertas_dias: 3
```

## Skills relacionados

| Skill | Descripción |
|-------|-------------|
| [`latam-timezone-briefing`](https://clawhub.ai/centriqs/latam-timezone-briefing) | Briefing matutino ART — integra vencimientos fiscales automáticamente |
| `afip-monitor` *(paid)* | Monitoreo en tiempo real de tu cuenta ARCA — disponible en [ClawMart](https://shopclawmart.com) |

## Notas importantes

- **ARCA (ex AFIP):** desde noviembre 2024, la AFIP opera bajo el nombre ARCA. Formularios y procedimientos sin cambios.
- **Validez legal:** las únicas fechas con validez oficial son las publicadas en [arca.gob.ar/vencimientos](https://arca.gob.ar/vencimientos). Este skill es orientativo.
- **Montos:** los valores de cuotas del Monotributo se actualizan semestralmente. Consultar ARCA para montos vigentes.

## Licencia

MIT — Libre uso, modificación y redistribución.

---

Desarrollado por **[Centriqs](https://centriqs.io)** — *Center of your operations*
Agentes IA para PyMEs en LATAM · Buenos Aires, Argentina
