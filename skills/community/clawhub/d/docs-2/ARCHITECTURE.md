# Arquitectura

Una sola narrativa con rutas de catálogo. El scroll es la cámara. No hay secciones sueltas: cada bloque es una escena y la señal cambia de trabajo.

```
src/i18n/es  src/i18n/en     capas de interfaz
src/data                       hechos: empresa, catálogo, proyectos, ingeniería
src/sections                   Hero, Signal, About, Engineering, Products, Projects, Contact
src/three/scenes               SignalScene (WebGL), EngineeringScene (dibujo), ProjectScene (profundidad)
src/components/immersive       sistema de imagen
src/components/motion          Lenis + canvas 2D
```

WebGL: un renderer, import dinámico, solo escritorio con puntero fino, se dispone al desmontar. Móvil y reduced motion usan el canvas 2D.

Rutas: `/`, `/en`, `/productos`, `/productos/:categoria`, `/producto/:slug` y el espejo en inglés.

La rama `immersive-redesign` pedida en el brief no se creó: esta sesión está fija a su rama de trabajo. `main` queda intacta.
