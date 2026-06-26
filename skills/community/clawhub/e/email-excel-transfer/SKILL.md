---
name: email-excel-transfer
description: Automatyzuje workflow pobierania danych z email i wstawiania ich do arkuszy kalkulacyjnych. Użyj gdy użytkownik chce przenieść informacje z poczty do Excela. Domyślnie działa na KOPIACH plików — oryginały pozostają nienaruszone.
---

# Email → Excel Transfer

Automatyczny workflow: pobierz dane z załącznika → przetwórz → wypełnij arkusz.

⚠️ **Bezpieczeństwo:** Domyślnie wszystkie operacje wykonywane są na KOPIACH plików. Oryginalne pliki pozostają nienaruszone.

## Wymagania
- OpenClaw z dostępem do email
- Microsoft Excel
- Opcjonalnie: MCP bridge do komunikacji z Windows

---

## Setup / Credentials

### 1. Hasło aplikacji do email

**NIE używaj** hasła do konta — stwórz **hasło aplikacji** (app password).

**Jak wygenerować hasło aplikacji:**
- Gmail: https://myaccount.google.com → Bezpieczeństwo → Hasła aplikacji
- Outlook/Hotmail: https://account.microsoft.com → Zabezpieczenia → Hasła aplikacji  
- WP Poczta: https://poczta.wp.pl → Ustawienia → Hasła aplikacji

### 2. Ograniczenie dostępu

Hasło aplikacji daje dostęp TYLKO do odczytu poczty — nie może zmienić hasła ani wyłączyć 2FA.

**Whitelista nadawców (opcjonalnie):**
Dodaj listę dozwolonych adresów email — skill zignoruje wiadomości od innych nadawców:
```python
DOZWOLENI_NADAWCY = ['kontakt@firma.pl', 'biuro@firma.pl']
```

---

## 1. Pobierz wiadomość email

```python
import imaplib, ssl, email, re

# === KONFIGURACJA ===
SERWER = 'imap.example.com'
PORT = 993
EMAIL = 'twoj@email.pl'
HASLO = 'xxxx xxxx xxxx xxxx'  # Hasło aplikacji, NIE zwykłe hasło

# Whitelista nadawców - zostaw puste [] żeby akceptować wszystkich
DOZWOLENI_NADAWCY = []

# Sanityzacja nazwy pliku - usuń wszystko poza bezpiecznymi znakami
def sanityzuj_nazwe(nazwa):
    if not nazwa:
        return None
    # Usuń ścieżki i niebezpieczne znaki
    nazwa = re.sub(r'[/\\]', '', nazwa)  # usuń slashe
    nazwa = re.sub(r'[^\w\s\-.]', '', nazwa)  # tylko bezpieczne znaki
    nazwa = nazwa[:200]  # max 200 znaków
    return nazwa.strip()

# === POBIERANIE WIADOMOŚCI ===
mail = imaplib.IMAP4_SSL(SERWER, PORT, ssl_context=ssl.create_default_context())
mail.login(EMAIL, HASLO)
mail.select('INBOX')

# Szukaj wiadomości (dowolny temat)
_, wiadomosci = mail.search(None, 'ALL')
id_wiadomosci = wiadomosci[0].split()
id_ostatniej = id_wiadomosci[-1]

_, dane = mail.fetch(id_ostatniej, '(RFC822)')
wiadomosc = email.message_from_bytes(dane[0][1])

# Sprawdź nadawcę
nadawca = wiadomosc.get('From', '')
if DOZWOLENI_NADAWCY and not any(n in nadawca for n in DOZWOLENI_NADAWCY):
    print(f"[BLOKADA] Nadawca {nadawca} nie jest na whitelisty")
    mail.logout()
    exit()

# Wyciągnij temat
temat = wiadomosc.get('Subject', '(bez tematu)')
print(f"Pobrano: {temat} od {nadawca}")
```

## 2. Wyciągnij załącznik

```python
# Zapisz TYLKO pierwszy pasujący plik
for czesc in wiadomosc.walk():
    if czesc.get_content_disposition() == 'attachment':
        nazwa = czesc.get_filename()
        nazwa = sanityzuj_nazwe(nazwa)  # sanityzacja!
        
        if nazwa and '.xlsx' in nazwa.lower():
            tresc = czesc.get_payload(decode=True)
            if tresc:
                # Zapisz do /tmp z prefixem "copy_"
                sciezka_kopia = f'/tmp/copy_{nazwa}'
                with open(sciezka_kopia, 'wb') as f:
                    f.write(tresc)
                print(f"Zapisano kopię: {sciezka_kopia}")
                break
```

## 3. Odczytaj komórki z xlsx

```python
import zipfile, re

def czytaj_xlsx(sciezka):
    with zipfile.ZipFile(sciezka) as z:
        arkusz = z.read('xl/worksheets/sheet1.xml').decode()
        teksty = z.read('xl/sharedStrings.xml').decode()
    
    wartosci = re.findall(r'<t[^>]*>([^<]+)</t>', teksty)
    komorki = re.findall(r'<c r="([A-Z]+\d+)"([^>]*)>(.*?)</c>', arkusz, re.DOTALL)
    
    dane = {}
    for ref, attr, cont in komorki:
        v = re.search(r'<v>([^<]+)</v>', cont)
        if v:
            val = v.group(1)
            if 't="s"' in attr:
                val = wartosci[int(val)]
            dane[ref] = val
    return dane
```

## 4. DRY-RUN / PREVIEW — pokaż zmiany przed zapisem

```python
def preview_zmian(sciezka, zmiany):
    """
    Wyświetla planowane zmiany do akceptacji.
    Zmiany to słownik: {(wiersz, kolumna): nowa_wartosc}
    """
    print("\n📋 PLANOWANE ZMIANY:")
    print("-" * 40)
    for komorka, wartosc in zmiany.items():
        print(f"  {komorka} → {wartosc}")
    print("-" * 40)
    print(f"Plik: {sciezka}")
    print("\nPotwierdź przed zapisem: tak/nie")

def dry_run(sciezka, zmiany):
    """Pokazuje zmiany ale NIE zapisuje."""
    preview_zmian(sciezka, zmiany)
    return False  # nie zapisuj

# Przykład użycia:
zmiany = {(6, 5): 2450000, (6, 6): 2380000}
akceptacja = dry_run('/tmp/copy_raport.xlsx', zmiany)
if not akceptacja:
    print("Anulowano — brak zapisu")
    exit()
```

## 5. Zapisz dane do Excela (NA KOPII)

Na Windows użyj PowerShell:

```powershell
# Otwórz PLIK KOPIĘ (nie oryginał!)
$excel = New-Object -ComObject Excel.Application
$excel.Visible = $false
$wb = $excel.Workbooks.Open("C:\temp\copy_raport.xlsx")  # copy_ prefix!
$ws = $wb.ActiveSheet

# Wstaw dane do komórki
$ws.Cells.Item(6, 5).Value2 = 2450000

# Zapisz i zamknij
$wb.Save()
$wb.Close($false)
$excel.Quit()

Write-Host "Zapisano pomyslnie: C:\temp\copy_raport.xlsx"
```

---

## Konfiguracja

1. **Hasło aplikacji** — wygeneruj w panelu swojego dostawcy email
2. **Whitelista nadawców** — dodaj zaufane adresy w kodzie
3. **Tryb dry-run** — włączony domyślnie, pokazuje zmiany przed zapisem
4. **MCP bridge** — opcjonalny do komunikacji Linux→Windows

---

## Użycie

```
1. Powiedz "pobierz dane z maila i wstaw do Excela"
2. Agent pobiera wiadomość → wyświetla PLAN ZMIAN (dry-run)
3. Potwierdzasz → agent zapisuje do pliku z prefixem "copy_"
4. Oryginalny plik pozostaje nietknięty
```

⚠️ **Ważne:** Wszystkie zmiany zapisywane są do plików z prefixem `copy_`. Oryginały nigdy nie są modyfikowane.
