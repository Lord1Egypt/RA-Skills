---
name: ai-coach
description: Coach de IA personalizado. Proporciona retroalimentación, establece metas y te motiva a mejorar continuamente.
metadata: {"openclaw":{"emoji":"🏆","auto":false}}
---

# AI Coach (Coach Personalizado)

Tu coach de IA disponible 24/7. Establece metas, recibe retroalimentación y mantente motivado.

## Capacidades

| Función | Descripción |
|---------|-------------|
| **Metas** | Define y rastrea objetivos |
| **Check-ins** | Evaluaciones periódicas |
| **Motivación** | Mensajes de ánimo personalizados |
| **Retroalimentación** | Análisis de progreso |
| **Hábitos** | Sugiere mejoras de rutina |

## Comandos

```
# Establecer meta
coach goal "Aprender Python en 3 meses"

# Check-in diario
coach checkin

# Reflexión semanal
coach weekly

# Pedir motivación
coach motivate

# Ver progreso
coach progress
```

## Ejemplo

```
Usuario: coach checkin

Bot: 🏆 Check-in del día:

     ¿Cómo estuvo tu día en una escala 1-10?
     [1-3] [4-6] [7-10]

Usuario: 7

Bot: 👍 ¡Buen día!

     📊 Revisión rápida:
     
     ✅ Completaste 4/5 tareas planificadas
     ✅ 2 pomodoros de enfoque
     ⚠️ No registraste ejercicio hoy
     
     💪 Lo que hiciste bien:
     • Mantuviste enfoque en el proyecto principal
     • Respondiste emails antes de las 10am
     
     🎯 Para mañana:
     • Intenta iniciar con la tarea más difícil
     • Programa 30 min de ejercicio
     
     💬 "El progreso, no la perfección, es lo que 
        debemos buscar." - Recuerda esto.
```

## Tipos de Coaching

| Área | Enfoque |
|------|---------|
| **Productividad** | Gestión del tiempo, enfoque |
| **Fitness** | Ejercicio, nutrición |
| **Aprendizaje** | Nuevas habilidades |
| **Carrera** | Desarrollo profesional |
| **Bienestar** | Salud mental, balance |

## Reflexión Semanal

```
Usuario: coach weekly

Bot: 🏆 Reflexión Semanal:

     📅 Esta semana (Feb 1-7):
     
     🎯 Metas vs Realidad:
     ├── Aprender Python: 65% → 72% (+7%)
     ├── Ejercicio: 4/5 días ✅
     └── Proyecto Alpha: Bloqueado ⚠️
     
     📈 Tendencias:
     • Productividad: ↑ 12% vs semana pasada
     • Enfoque: Mejor por las mañanas
     • Energía: Baja los miércoles
     
     💡 Sugerencias para próxima semana:
     1. Programa trabajo creativo en la mañana
     2. Toma descanso activo los miércoles
     3. Divide el bloqueo de Proyecto Alpha
     
     🌟 Momento destacado: Completaste el 
        módulo de funciones en Python
```

## Configuración

```bash
COACH_CHECKIN_TIME=21:00
COACH_WEEKLY_DAY=sunday
COACH_PERSONALITY=supportive  # supportive, direct, challenging
```

## Integración

- **habit-tracker**: Analiza hábitos para coaching
- **task-manager**: Evalúa productividad
- **daily-digest**: Incluye tips diarios
- **personality-modes**: Adapta tono del coach
