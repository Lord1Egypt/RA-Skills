# Registration Search Queries

Run these query batches in sequence. Each batch targets a different language or signal type.
For IMAP, each line is a separate `SEARCH SUBJECT "..."` command.
For Gmail, combine terms with `OR` inside `subject:(...)`.

---

## Batch 1 – English

```
welcome
account created
confirm your email
verify your email
verify your account
activate your account
you're registered
successfully registered
thanks for signing up
thank you for registering
you have subscribed
subscription confirmed
your account is ready
complete your registration
finish your registration
one more step
almost there
```

Gmail query:
```
subject:(welcome OR "account created" OR "confirm your email" OR "verify your email" OR "activate your account" OR "successfully registered" OR "thanks for signing up" OR "you have subscribed")
```

---

## Batch 2 – German

```
willkommen
konto erstellt
e-mail bestätigen
e-mail-adresse bestätigen
konto bestätigen
registrierung bestätigen
erfolgreich registriert
anmeldung bestätigt
danke für deine registrierung
danke für deine anmeldung
fast geschafft
nur noch ein schritt
ihr konto ist bereit
herzlich willkommen
```

Gmail query:
```
subject:(willkommen OR "konto erstellt" OR "e-mail bestätigen" OR "registrierung bestätigen" OR "erfolgreich registriert" OR "danke für deine registrierung" OR "herzlich willkommen")
```

---

## Batch 3 – French

```
bienvenue
compte créé
confirmez votre adresse
vérifiez votre e-mail
activez votre compte
inscription confirmée
vous êtes inscrit
merci de votre inscription
votre compte est prêt
finaliser votre inscription
encore une étape
```

Gmail query:
```
subject:(bienvenue OR "compte créé" OR "confirmez votre adresse" OR "vérifiez votre e-mail" OR "activez votre compte" OR "inscription confirmée" OR "merci de votre inscription")
```

---

## Batch 4 – Spanish

```
bienvenido
bienvenida
cuenta creada
confirma tu correo
verifica tu cuenta
activa tu cuenta
registro exitoso
gracias por registrarte
tu cuenta está lista
completar registro
un paso más
```

Gmail query:
```
subject:(bienvenido OR bienvenida OR "cuenta creada" OR "confirma tu correo" OR "verifica tu cuenta" OR "registro exitoso" OR "gracias por registrarte")
```

---

## Batch 5 – Italian

```
benvenuto
benvenuta
account creato
conferma la tua email
verifica il tuo account
attiva il tuo account
registrazione completata
grazie per la registrazione
il tuo account è pronto
```

Gmail query:
```
subject:(benvenuto OR benvenuta OR "account creato" OR "conferma la tua email" OR "verifica il tuo account" OR "registrazione completata" OR "grazie per la registrazione")
```

---

## Batch 6 – Portuguese

```
bem-vindo
bem-vinda
conta criada
confirme o seu email
verifique o seu email
ative a sua conta
registro confirmado
obrigado por se registrar
a sua conta está pronta
```

Gmail query:
```
subject:(bem-vindo OR bem-vinda OR "conta criada" OR "confirme o seu email" OR "verifique o seu email" OR "registro confirmado" OR "obrigado por se registrar")
```

---

## Batch 7 – Dutch

```
welkom
account aangemaakt
bevestig je e-mailadres
verifieer je account
activeer je account
registratie bevestigd
bedankt voor je registratie
je account is klaar
```

Gmail query:
```
subject:(welkom OR "account aangemaakt" OR "bevestig je e-mailadres" OR "activeer je account" OR "registratie bevestigd" OR "bedankt voor je registratie")
```

---

## Batch 8 – Polish

```
witamy
konto zostało utworzone
potwierdź swój adres e-mail
zweryfikuj konto
aktywuj konto
rejestracja potwierdzona
dziękujemy za rejestrację
twoje konto jest gotowe
```

Gmail query:
```
subject:(witamy OR "konto zostało utworzone" OR "potwierdź swój adres" OR "rejestracja potwierdzona" OR "dziękujemy za rejestrację")
```

---

## Batch 9 – Turkish

```
hoş geldiniz
hesabınız oluşturuldu
e-postanızı doğrulayın
hesabınızı doğrulayın
hesabınızı etkinleştirin
kayıt onaylandı
kayıt olduğunuz için teşekkürler
hesabınız hazır
```

Gmail query:
```
subject:(hoş geldiniz OR "hesabınız oluşturuldu" OR "e-postanızı doğrulayın" OR "kayıt onaylandı" OR "kayıt olduğunuz için teşekkürler")
```

---

## Batch 10 – Universal Patterns (all languages)

These subject-line patterns are language-agnostic and catch remaining registrations:

```
noreply
no-reply
donotreply
do-not-reply
```

For IMAP, search sender (`FROM`) not subject:
```
SEARCH FROM "noreply"
SEARCH FROM "no-reply"
SEARCH FROM "donotreply"
```

For Gmail:
```
from:(noreply OR no-reply OR donotreply) subject:(welcome OR confirm OR verify OR register OR activate OR subscri)
```

---

## Signals to Exclude (Noise Reduction)

Skip emails matching these patterns to reduce false positives:

- Subject contains: `password reset`, `passwort vergessen`, `mot de passe oublié`, `forgot password`, `invoice`, `rechnung`, `receipt`, `order`, `bestellung`, `shipment`, `delivery`, `unsubscribe`, `abmelden`
- Sender domain matches known transactional-only senders (payment processors, shipping companies)
- No company name extractable from sender or subject
