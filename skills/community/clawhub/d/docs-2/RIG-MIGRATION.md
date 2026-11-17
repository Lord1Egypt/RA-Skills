# Migración al rig §17 — r3f-scroll-rig + three-story-controls

Decisión aprobada por la persona (2026-10-02): instalar ambos.

## Estado (2026-10-03) — paso 2 EJECUTADO

La escena 01 SIGNAL corre ya sobre el rig global tras el flag `VITE_RIG=r3f`:

- `src/three/rig.ts` — `RIG_R3F` + `useRigDisponible()`: flag de entorno +
  WebGL + puntero fino + no-móvil + no-reduced-motion. Si algo falla, el sitio
  funciona como antes.
- `src/three/GlobalRig.tsx` — `GlobalCanvas` único, fijo, carga diferida
  (`import()`), con el encuadre y la niebla de `SignalCanvas` para que el
  campo no cambie de aspecto al cambiar de host.
- `src/three/SignalRig.tsx` — `ScrollScene` trackea el lienzo DOM
  (`data-3d="signal-field"`). El GLSL de `SignalField` NO se tocó.
- `src/scenes/Signal.tsx` — elige camino: rig (si disponible) o
  `SignalCanvas` con su fallback 2D. Módulo del rig importado sólo si se usa.
- `src/App.tsx` — monta `<GlobalRig />` una vez, en lazy.

## Decisiones registradas

- **frameloop demand (§17.5) aplazado para el paso de cámaras.** El campo de
  señal es animación continua (estado vivo, DNA §1.4): `useFrame` necesita el
  loop. `frameloop="demand"` entra cuando las escenas estáticas usen el rig
  (DOM-sync de imágenes, transiciones de cámara con three-story-controls).
- **Lenis propio se conserva.** No se pasa `friction` al rig; el scroll
  suave sigue siendo el de siempre (lerp 0.085, DNA §7). Si se detectara doble
  suavizado en QA, se apaga el de r3f o el nuestro — se mide antes de tocar.
- `three-story-controls` entra en el paso 3 (pasajes de cámara entre escenas),
  no en este.

## Cómo probarlo

```bash
VITE_RIG=r3f npm run dev     # rig activo
npm run dev                  # camino por defecto (sin rig)
```

Verificar (Design Loop, §14): campo idéntico en 01 · 0 errores de consola
ES/EN · bundle inicial sin el rig ≤ 120 KB gzip · 0 overflow 360px (móvil ni
sabe que el rig existe).

## Orden de migración (no big-bang)

1. ~~Instalar deps~~ (hecho).
2. ~~Escena 01 SIGNAL sobre el rig~~ (hecho — este commit).
3. QA del paso 2: lint + typecheck + qa + visual en escritorio real.
4. Si 01 pasa el Design Loop: extender a 00 (Entry) y 03 (Engineering);
   entonces `frameloop="demand"` y `three-story-controls` (pasajes de cámara).
5. Cada paso es un commit por hito.

## Reglas innegociables

- La cámara avanza con el scroll; la imagen no se deforma (ref Da7ZuhyWACg).
- Nada rebota; easings power2.out (ref 3eExfC63uSc).
- Reduced-motion y móvil: SIEMPRE fallback narrativo, nunca página muerta.
- Las dos piezas propias (propagación física del 01, diagrama polar del 03)
  se conservan tal cual: son el DNA diferencial.
