# BET - Biztonsági és Egészségvédelmi Terv Skill

## Leírás
Biztonsági és Egészségvédelmi Terv (BET) generálása építési/kivitelezési projektekhez a magyar jogszabályi követelményeknek megfelelően.

## Jogszabályi háttér
- **1993. évi XCIII. törvény** a munkavédelemről
- **4/2002. (II. 20.) SzCsM-EüM együttes rendelet** - BET kötelező tartalom
- **355/2005. (XII. 31.) Korm. rendelet** - építési kivitelezés
- **22/2005. (VI. 24.) EüM rendelet** - munkavédelmi követelmények

## Mikor kötelező?
- Építési engedély alapján történő kivitelezésnél
- Több munkáltató egyidejű jelenléte esetén
- A kivitelezés nem kezdhető el BET nélkül!

## Kinek kell elkészítenie?
- **Tervező** köteles készíteni a kiviteli tervdokumentáció részeként
- **Tervezési koordinátor** szakmai ellenőrzése
- Gyakorlatban gyakran a **kivitelező munkavédelmi szakembere** készíti

## Kötelező tartalmi elemek

### 1. Alapadatok
- Megrendelő neve, címe, elérhetősége
- Tervkészítő neve, jogosultsága, elérhetősége
- Tervezett munka rövid leírása
- Kiviteli terv azonosító jele
- Építés helye, jellege

### 2. Jogszabályi hivatkozások
- Munkavédelmi törvények felsorolása
- Szabványok hivatkozása
- Ágazati specifikus előírások

### 3. Felvonulási terület szabályai
- Megközelíthetőség
- Elkerítés, őrzés
- Energiaellátás, megvilágítás
- Belső utak, parkolók
- Közműellátás
- Villámvédelem, tűzvédelem
- Menekülési utak
- Anyagtárolás biztonsági előírásai

### 4. Konkrét kivitelezési munkák
- Munkaárkok, instabil szerkezetek dúcolása
- Gépek, berendezések telepítése
- Leesés elleni védelem (kollektív előnyben)
- Anyagmozgatás megoldása
- Magasban végzett munka biztonsága
- Állványok, zsaluzatok
- Emelőgépek használata

### 5. Fokozott veszélyt jelentő munkák (kötelező!)
A 4/2002. rendelet 2. számú melléklete alapján:
- Talajmegcsúszás, betemetés veszélye
- Veszélyes anyagok expozíciója
- Foglalkozási sugárterhelés
- Nagyfeszültségű vezetékek közelében végzett munka
- Elektromágneses sugárzás kockázata
- Vízbefúlás veszélye
- Árokban, alagútban, földalatti munka
- Légellátó rendszerrel rendelkező búvárok munkája
- Keszonban, túlnyomásban végzett munka
- Robbanóanyagok használata
- Nehéz előre gyártott elemek szerelése

### 6. Megelőző intézkedések
- Kockázatértékelés
- Egyéni védőeszközök
- Kollektív védelmi megoldások
- Oktatások, tájékoztatások
- Tűzvédelmi intézkedések
- Elsősegélynyújtás szervezése
- Hulladékkezelés

### 7. Szervezeti háttér
- Fővállalkozó, alvállalkozók listája
- Koordinátorok kijelölése
- Kapcsolattartási útvonalak
- Veszélyhelyzeti eljárásrend

## Használat
```
/bet --partner <név> --helyszín <cím> --munka <leírás>
```

## Kimenő formátumok
- `.docx` - szerkeszthető szabályzat
- `.pdf` - végleges dokumentum
- `.xlsx` - kockázatértékelési nyilvántartás

## FIGYELMEZTETÉS
Ez a skill nem helyettesíti a minősített munkavédelmi szakember véleményét. Jogi tanácsadásra nem alkalmas.
