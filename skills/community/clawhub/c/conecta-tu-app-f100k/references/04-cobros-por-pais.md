# 04 · Cobrar según tu país

Verificado el **15-sep-2026** en las páginas oficiales (fuentes abajo). Esto cambia: si la fecha tiene más de 3 meses, Claude vuelve a revisar las fuentes antes de recomendar.

## Primero: dos formas de cobrar

- **Cobras tú** (Stripe, Mercado Pago, PayPal): la cuenta está a tu nombre, tú facturas y tú declaras. Las comisiones son más bajas, pero **solo puedes abrirla si tu país está en su lista**.
- **Cobran por ti** ("merchant of record": Lemon Squeezy, Polar, Paddle, Hotmart, Gumroad): la plataforma vende en tu nombre, se encarga de los impuestos de cada país del comprador y te paga a tu banco o PayPal. La comisión es más alta, pero **funciona desde casi cualquier país**, sin empresa en EE. UU.

## ¿Qué me conviene? Por país

| Vives en… | Opción directa | Opción "cobran por ti" | Nota |
|---|---|---|---|
| **México** | **Stripe** ✅ · Mercado Pago ✅ (con suscripciones) | Lemon Squeezy, Polar, Hotmart | Stripe es lo más simple para suscripciones con tarjeta. |
| **Brasil** | **Stripe** ✅ · Mercado Pago ✅ | Hotmart, Paddle | Polar y el pago a banco de Lemon Squeezy **no** incluyen Brasil. |
| **España** | **Stripe** ✅ | Lemon Squeezy, Polar, Paddle | Stripe Managed Payments (Stripe cobra por ti) también está disponible en España. |
| **EE. UU.** | **Stripe** ✅ | Todas | — |
| **Colombia, Perú, Chile, Argentina, Uruguay** | **Mercado Pago** ✅ (con suscripciones) · ❌ **sin Stripe directo** | Polar, Lemon Squeezy, Paddle, Hotmart | Mercado Pago cobra en moneda local. Para vender en dólares a otros países: Polar o Lemon Squeezy. |
| **Ecuador, Bolivia, Paraguay, Guatemala, Costa Rica, Panamá, Rep. Dominicana, El Salvador** | ❌ sin Stripe ni Mercado Pago | **Polar** o **Lemon Squeezy** (te pagan a tu banco) · Paddle · Hotmart | Bolivia y Paraguay **no** están en la tabla de países de PayPal Payouts. |
| **Honduras** | ❌ | Paddle · Hotmart · **PayPal** | No aparece en Polar ni en el pago a banco de Lemon Squeezy (sí vía PayPal). |
| **Venezuela** | ❌ | **PayPal** (recibe y retira) · Lemon Squeezy pagando **a PayPal** | Paddle excluye Venezuela, y no está en Polar ni en el pago a banco de Lemon Squeezy. |

**¿Y abrir una empresa en EE. UU. con Stripe Atlas?** Cuesta **USD 500 una vez + USD 100 al año** (más contador e impuestos de EE. UU.). Conviene cuando ya vendes en serio y las comisiones del "cobran por ti" pesan. Para empezar no hace falta.

## Comisiones de referencia (15-sep-2026)

| Plataforma | Comisión por venta | Extra |
|---|---|---|
| Lemon Squeezy | 5% + USD 0,50 | +1,5% internacional · +0,5% suscripciones · retiro a banco fuera de EE. UU. 1% |
| Polar | 5% + USD 0,50 | +1,5% tarjetas no estadounidenses · retiro USD 2/mes + 0,25% + USD 0,25 |
| Paddle | 5% + USD 0,50 | — |
| Gumroad | 10% + USD 0,50 | 30% si la venta llega por su marketplace |
| Hotmart | ~9,9% + un fijo por venta | el fijo exacto no quedó claro en su página |
| Stripe / Mercado Pago | depende del país | ver su página de precios local |

**Lemon Squeezy en 2026:** fue comprada por Stripe y publicó una actualización sobre migrar a Stripe Managed Payments. Sigue aceptando registros, pero su futuro no está confirmado oficialmente. Si empiezas hoy desde LatAm sin Stripe, **Polar** es la alternativa con menos incertidumbre.

## Cómo se conecta el cobro con el portero

Sea cual sea la plataforma, **siempre es lo mismo**:
1. **Botón de pago**: un link de pago de la plataforma (Stripe Payment Link, link de suscripción de Mercado Pago, checkout de Polar o Lemon Squeezy). **No hace falta programar el checkout.**
2. **Aviso de pago**: la plataforma llama a tu webhook → el correo entra a `miembros_activos`.
3. **Aviso de cancelación**: el webhook lo quita, o el refresco diario lo corrige.

Dos reglas de seguridad que Claude no se salta:
- **Verificar que el aviso es real.** Stripe firma cada aviso (`constructEvent` con el cuerpo crudo). Mercado Pago avisa con un id: **consulta ese id en su API** antes de dar acceso, nunca le creas al cuerpo del aviso. Polar y Lemon Squeezy también firman.
- **Probar en modo prueba primero.** Stripe tiene tarjetas de prueba (`4242 4242 4242 4242`) y `stripe listen --forward-to localhost:3000/api/webhooks/stripe` para recibir avisos en tu compu. Mercado Pago tiene usuarios de prueba. Nada pasa a producción sin una compra de prueba que haya terminado **con el correo dentro de la lista**.

## Fuentes (15-sep-2026)

stripe.com/global · stripe.com/atlas · docs.stripe.com/payments/managed-payments/eligibility · mercadopago.com.ar/developers/es/docs/checkout-pro/overview · mercadopago.com.ar/developers/es/docs/subscriptions/overview · docs.lemonsqueezy.com/help/getting-started/supported-countries · docs.lemonsqueezy.com/help/getting-started/fees · polar.sh/docs/merchant-of-record/supported-countries · paddle.com/pricing · gumroad.com/pricing · hotmart.com/es/precios · developer.paypal.com/docs/payouts/standard/reference/country-feature/
