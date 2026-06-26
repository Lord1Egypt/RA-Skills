# Skill: Consultoría IA 🦞

Sistema completo de consultoría en inteligencia artificial para PYMES, desarrollado por Marcelo Bustos (Argentina) con asistencia de Pepper.

## 🚀 Características principales

### 🎯 Diagnóstico McKinsey
- Entrevistas estructuradas (MECE, Issue Tree, 5 Whys)
- Análisis preliminar automatizado
- Cálculo de ROI preliminar
- Guías de preguntas por vertical (retail, salud, logística)

### 🛠️ Desarrollo de Soluciones
- Flujo completo: Discovery → Prototipo → Implementación → Operación
- Stack tecnológico recomendado por etapa (Starter/Growth/Enterprise)
- Templates reutilizables de propuestas y planes

### 📊 Seguimiento y ROI
- Métricas de éxito definidas
- Dashboard de KPIs automático
- Cálculo de ROI real vs estimado
- Alertas de problemas y oportunidades

## 👥 Agentes especializados incluidos

### 1. 🎯 Agente Diagnosticador
- Realiza entrevistas tipo McKinsey
- Identifica problemas y oportunidades
- Calcula ROI preliminar
- **Modelo recomendado:** Claude Sonnet

### 2. 🛠️ Agente Desarrollador
- Diseña soluciones técnicas
- Recomienda stack tecnológico
- Estima tiempo/costo
- **Modelo recomendado:** GPT-4

### 3. 📊 Agente Analista
- Monitorea métricas de éxito
- Genera reportes de ROI
- Sugiere mejoras continuas
- **Modelo recomendado:** Claude Haiku (costo-efectivo)

## 📁 Estructura del skill

```
consultoria-ia/
├── SKILL.md              # Documentación principal
├── README.md             # Este archivo
├── package.json          # Metadatos
├── RESUMEN-EJECUTIVO.md  # Visión general del sistema
├── flujo-entrevistas-mckinsey.md    # Flujo 1: Diagnóstico
├── flujo-desarrollo-soluciones.md   # Flujo 2: Desarrollo
├── agentes/              # Agentes especializados
│   ├── agente-diagnosticador.md
│   ├── agente-desarrollador.md
│   └── agente-analista.md
├── templates/            # Plantillas reutilizables
│   └── analisis-preliminar.md
└── checklists/           # Listas de verificación
    └── preparacion-entrevista.md
```

## 🎯 Casos de uso típicos

### Para PYMES argentinas:
- **Retail:** Optimización inventario, recomendación productos
- **Salud:** Gestión historias clínicas, agendamiento automático
- **Logística:** Optimización rutas, predicción demanda
- **Servicios:** Automatización atención al cliente, procesamiento documentos

### Para consultores:
- **Metodología estructurada** lista para usar
- **Templates profesionales** para propuestas
- **Herramientas de medición** de impacto real
- **Sistema escalable** de un cliente a muchos

## 🔧 Instalación

```bash
# Instalar desde ClawHub
clawhub install consultoria-ia

# O instalar manualmente
git clone https://github.com/tu-usuario/consultoria-ia-skill.git
cp -r consultoria-ia-skill/ ~/.openclaw/skills/
```

## 🚀 Uso rápido

### Ejemplo 1: Diagnóstico rápido
```bash
# En conversación con OpenClaw
/consultoria diagnosticar "MiTienda" retail
```

### Ejemplo 2: Propuesta de solución
```bash
/consultoria proponer-solucion "predicción de demanda"
```

### Ejemplo 3: Seguimiento
```bash
/consultoria estado-proyecto "proyecto-001"
```

## 📊 Métricas de éxito definidas

### Para diagnóstico (Flujo 1):
- **Tiempo preparación:** <2h por entrevista
- **Tasa conversión entrevista → propuesta:** >40%
- **Satisfacción cliente (NPS):** >8

### Para desarrollo (Flujo 2):
- **Tiempo MVP:** <4 semanas
- **ROI documentado:** >2x en primeros 3 meses
- **Uptime producción:** >99.5%
- **Retención cliente a 6 meses:** >80%

## 🔗 Integraciones

### Con Mission Control (OpenClaw)
- Crea tareas automáticamente
- Sincroniza estado de proyectos
- Notifica fechas límite

### Con sistema de costos
- Calcula costo de soluciones
- Sugiere optimizaciones
- Alertas de presupuesto

### Con memoria vectorizada
- Recupera casos similares
- Sugiere templates basados en contexto
- Aprende de proyectos anteriores

## 🌎 Contexto argentino

Este skill está especialmente diseñado para el mercado argentino:

### Consideraciones locales:
- **AFIP:** Integración con sistemas tributarios
- **MercadoLibre:** APIs de e-commerce local
- **Bancos argentinos:** APIs de pagos
- **Normativas:** Ley de protección de datos personal

### Pricing adaptado:
- **Starter:** $5,000 - $15,000 ARS
- **Growth:** $15,000 - $50,000 ARS  
- **Enterprise:** $50,000+ ARS

## 🛠️ Configuración recomendada

### Variables de entorno:
```bash
export CONSULTORIA_VERTICAL_PRINCIPAL="retail"
export CONSULTORIA_PRECIO_HORA=15000  # ARS
export CONSULTORIA_ROI_MINIMO=2.0
```

### Modelos por defecto:
```yaml
diagnosticador:
  model: claude-3-5-sonnet-20241022
  temperature: 0.3

desarrollador:
  model: gpt-4-turbo-preview  
  temperature: 0.4

analista:
  model: claude-3-haiku-20240307
  temperature: 0.2
```

## 📈 Roadmap

### Versión 1.0 (Actual)
- ✅ Flujos básicos documentados
- ✅ Templates reutilizables
- ✅ Agentes especializados
- ✅ Integración Mission Control

### Versión 1.1 (Próxima)
- Dashboard de métricas
- Auto-aprendizaje de casos
- Fine-tuning para verticales específicas

### Versión 2.0 (Futuro)
- Marketplace de soluciones pre-construidas
- Equipo virtual de consultores IA
- Certificaciones y training

## 👨‍💻 Autor

**Marcelo Bustos** (mgbustos70@gmail.com)
- Consultor IA con experiencia real en PYMES argentinas
- 2+ años implementando soluciones de IA
- Especializado en retail, salud y logística

**Asistente:** Pepper 🦞 (Agente OpenClaw)

## 📄 Licencia

Creative Commons Attribution-NonCommercial 4.0 International

Puedes usar, modificar y distribuir este skill con atribución.
No comercial sin permiso del autor.

## 🤝 Contribuciones

¡Bienvenidas contribuciones! Áreas prioritarias:
1. Templates para nuevas verticales
2. Integraciones con APIs argentinas
3. Mejoras en cálculo de ROI
4. Traducciones a otros idiomas

## 🐛 Reportar problemas

Issues en GitHub: https://github.com/mgbustos/consultoria-ia-skill/issues

O contactar a: mgbustos70@gmail.com

---
**Publicado:** Abril 2026  
**Versión:** 1.0.0  
**Estado:** Activo y en uso real  
**Instalaciones:** [Contador de ClawHub]