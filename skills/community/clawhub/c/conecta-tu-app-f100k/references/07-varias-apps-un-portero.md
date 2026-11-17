# 07 · Varias apps, un solo portero (avanzado)

Úsalo **solo** cuando ya tienes 2 o más apps en dominios distintos y no quieres montar Supabase y la lista en cada una.

## La idea

Una app "central" (tu hub) tiene el login y la lista. Las demás apps **no tienen base de datos**. Solo confían en un **pase firmado** que emite el hub:

```
Persona en el hub (ya logueada y en la lista)
  → clic en "Abrir App B" → hub /api/abrir/app-b
      revisa la lista → firma un pase { email, app: 'app-b', vence: +24 h }
      → redirige a  https://app-b.com/__pase?t=<pase>
App B
  → verifica la firma con el secreto compartido + que app === 'app-b' + que no venció
  → guarda una cookie httpOnly de 24 h → deja pasar
  → si alguien abre App B directo, sin cookie → lo manda al hub, que vuelve a emitir el pase
```

## Decisiones que ya están probadas

- **Firma HS256** con un secreto compartido (`GATE_SECRET`, generado con `openssl rand -hex 32`) en el hub y en cada app. Librería: `jose` (`SignJWT` / `jwtVerify`).
- **Pase de 24 h, sin renovación silenciosa.** Cuando vence, un clic en el hub lo renueva. Si alguien cancela, en menos de 24 h pierde el acceso a las apps.
- **Cada pase dice para qué app es** (`app: 'app-b'`). Un pase de la App B no abre la App C.
- **`next` solo acepta rutas internas** (empiezan con `/` y no con `//`). Si no, alguien podría usar tu hub para redirigir a un sitio falso.
- **Las rutas de la app que gastan dinero** (llamadas a IA) vuelven a verificar la cookie en el servidor. No alcanza con que lo haga el proxy.

Claude arma esto con la skill abierta sobre los dos proyectos (hub y app). Es la misma lógica del portero, con un paso más.
