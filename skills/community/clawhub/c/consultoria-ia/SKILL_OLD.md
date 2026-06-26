# Skill: Consultoría IA

## Descripción
Sistema completo de consultoría en inteligencia artificial para PYMES. Incluye metodología McKinsey para diagnóstico, desarrollo de soluciones personalizadas, y seguimiento de ROI.

## Uso
```bash
# Instalar desde ClawHub
clawhub install consultoria-ia

# Usar en conversación
/consultoria diagnosticar [empresa] [vertical]
/consultoria proponer-solucion [problema]
/consultoria calcular-roi [inversion] [beneficio-esperado]
```

## Características

### 🎯 Diagnóstico McKinsey
- Entrevistas estructuradas (MECE, Issue Tree, 5 Whys)
- Análisis preliminar automatizado
- Guías de preguntas por vertical (retail, salud, logística)

### 🛠️ Desarrollo de Soluciones
- Flujo completo: Discovery → Prototipo → Implementación → Operación
- Stack tecnológico recomendado por etapa
- Templates reutilizables

### 📊 Seguimiento y ROI
- Métricas de éxito definidas
- Dashboard de KPIs
- Cálculo automático de ROI

## Archivos incluidos

### Documentación principal
- `RESUMEN-EJECUTIVO.md` - Visión general del sistema
- `flujo-entrevistas-mckinsey.md` - Flujo 1: Diagnóstico
- `flujo-desarrollo-soluciones.md` - Flujo 2: Desarrollo

### Templates
- `templates/analisis-preliminar.md` - Análisis pre-entrevista
- `templates/propuesta-comercial.md` - Propuesta formal
- `templates/plan-implementacion.md` - Plan detallado

### Checklists
- `checklists/preparacion-entrevista.md` - Preparación entrevista
- `checklists/validacion-cliente.md` - Validación con cliente
- `checklists/entrega-proyecto.md` - Entrega final

## Agentes especializados

### 🎯 Agente Diagnosticador
- Realiza entrevistas tipo McKinsey
- Identifica problemas y oportunidades
- Calcula ROI preliminar

### 🛠️ Agente Desarrollador
- Diseña soluciones técnicas
- Recomienda stack tecnológico
- Estima tiempo/costo

### 📊 Agente Analista
- Monitorea métricas de éxito
- Genera reportes de ROI
- Sugiere mejoras continuas

## Integraciones

### Con Mission Control
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

## Configuración

### Variables de entorno
```bash
CONSULTORIA_VERTICAL_PRINCIPAL="retail"
CONSULTORIA_PRECIO_HORA=150
CONSULTORIA_ROI_MINIMO=2.0
```

### Modelos recomendados
- **Diagnóstico:** Claude Sonnet (calidad)
- **Desarrollo:** GPT-4 o equivalente
- **Análisis:** Haiku (costo-efectivo)

## Ejemplos de uso

### Ejemplo 1: Diagnóstico rápido
```
Usuario: /consultoria diagnosticar "MiTienda" retail
Agente: 🎯 Analizando negocio de retail...
       • Preguntas clave: rotación de inventario, experiencia cliente, datos de ventas
       • Métricas a cuantificar: CAC, LTV, conversión
       • ROI potencial estimado: 3.5x en 6 meses
```

### Ejemplo 2: Propuesta de solución
```
Usuario: /consultoria proponer-solucion "predicción de demanda"
Agente: 🛠️ Solución recomendada:
       • Modelo: Series temporales + ML
       • Stack: Python, FastAPI, PostgreSQL
       • Timeline: 3 semanas para MVP
       • Costo estimado: $4,500
```

### Ejemplo 3: Seguimiento
```
Usuario: /consultoria estado-proyecto "proyecto-001"
Agente: 📊 Estado actual:
       • Fase: Implementación (70% completo)
       • ROI actual: 1.8x (proyectado: 3.2x)
       • Próximo hito: Capacitación equipo (15/04)
       • Alertas: Ninguna
```

## Roadmap

### Versión 1.0 (Actual)
- Flujos básicos documentados
- Templates reutilizables
- Integración con Mission Control

### Versión 1.1 (Próxima)
- Agentes especializados
- Dashboard de métricas
- Auto-aprendizaje de casos

### Versión 2.0 (Futuro)
- Fine-tuning de modelos específicos
- Marketplace de soluciones
- Equipo virtual de consultores

## Autor
Marcelo Bustos (magabu) con Pepper 🦞

## Licencia
Creative Commons Attribution-NonCommercial 4.0

---
**Instalado:** $(date +%Y-%m-%d)
**Versión:** 1.0.0
**Estado:** Activo