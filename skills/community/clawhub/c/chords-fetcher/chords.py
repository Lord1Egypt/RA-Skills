import sys
import urllib.request
from bs4 import BeautifulSoup
import re
from ddgs import DDGS

from urllib.parse import urlparse

ALLOWED_HOSTS = {"mychords.net", "amdm.ru", "www.amdm.ru", "ultimate-guitar.com", "tabs.ultimate-guitar.com"}

def search_chords(query):
    sites = ["mychords.net", "amdm.ru/akkordi", "ultimate-guitar.com/tabs"]
    
    for site in sites:
        try:
            # Добавляем слово "chords" или "аккорды" для более точного поиска
            search_query = f"site:{site} {query} chords" if "ultimate" in site else f"site:{site} {query} аккорды"
            results = DDGS().text(search_query, max_results=5)
            
            for r in results:
                href = r.get('href', '')
                
                # Проверяем, что URL начинается с http(s) и хост в allow-list
                if not href.startswith(('http://', 'https://')):
                    continue
                parsed = urlparse(href)
                if parsed.hostname and parsed.hostname not in ALLOWED_HOSTS:
                    continue
                
                # Проверяем, что хотя бы часть запроса есть в URL
                url_parts = href.lower().replace('-', '').replace('_', '')
                if not any(word in url_parts for word in query.lower().split()):
                    continue
                    
                if 'mychords.net/' in href and '/video/' not in href and 'nemeckom' not in href and 'ukrayinskoyu' not in href:
                    return href, 'mychords'
                elif 'amdm.ru/akkordi/' in href:
                    return href, 'amdm'
                elif 'ultimate-guitar.com/tabs/' in href and 'ultimate-guitar.com/pro/' not in href:
                    return href, 'ultimate-guitar'
        except Exception as e:
            print(f"Error searching DuckDuckGo for {site}: {e}")
            
    return None, None

def get_chords(url, site_type):
    headers = {
        'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/120.0.0.0 Safari/537.36',
        'Accept': 'text/html,application/xhtml+xml,application/xml;q=0.9,image/avif,image/webp,image/apng,*/*;q=0.8,application/signed-exchange;v=b3;q=0.7',
        'Accept-Language': 'ru-RU,ru;q=0.9,en-US;q=0.8,en;q=0.7',
    }
    
    try:
        req = urllib.request.Request(url, headers=headers)
        with urllib.request.urlopen(req, timeout=10) as response:
            html = response.read().decode('utf-8')
    except Exception as e:
        return f"Error fetching chords: {e}"

    soup = BeautifulSoup(html, 'html.parser')
    text = ""
    
    if site_type == 'mychords':
        div = soup.find('div', class_='w-words__text')
        if not div:
            return "Chords block not found on mychords.net."
            
        for br in div.find_all('br'):
            br.replace_with('\n')
            
        for a in div.find_all('a', class_='b-chord'):
            a.replace_with(f" {a.get_text()} ")
            
        text = div.get_text()
        
        chord_pattern = re.compile(r'([А-Яа-яa-z])([A-G][m#b7]*)')
        text = chord_pattern.sub(r'\1 \2', text)
        
        chord_pattern_after = re.compile(r'([A-G][m#b7]*)([А-Яа-яA-Z])')
        text = chord_pattern_after.sub(r'\1 \2', text)
        
    elif site_type == 'amdm':
        pre = soup.find('pre', itemprop='chordsBlock')
        if not pre:
            return "Chords block not found on amdm.ru."
        text = pre.get_text()
        
    elif site_type == 'ultimate-guitar':
        # Ultimate Guitar хранит аккорды в JSON внутри тега <script>
        script = soup.find('script', text=re.compile(r'window\.UGAPP\.store\.page'))
        if script:
            match = re.search(r'&quot;tab_view&quot;:{&quot;wiki_tab&quot;:{&quot;content&quot;:&quot;(.*?)&quot;', script.string)
            if match:
                text = match.group(1).replace('\\r\\n', '\n').replace('\\n', '\n')
                # Очистка от тегов [ch] и [/ch]
                text = re.sub(r'\[/?ch\]', '', text)
                text = re.sub(r'\[/?tab\]', '', text)
        if not text:
            return "Chords block not found on ultimate-guitar.com."

    # Очистка от табов
    lines = text.split('\n')
    cleaned_lines = []
    
    tab_pattern = re.compile(r'^\s*[eBGDAE1-6]?\|[-0-9hps/\\*x]+', re.IGNORECASE)
    tab_pattern2 = re.compile(r'\|-.*-\|')
    
    for line in lines:
        if tab_pattern.match(line) or tab_pattern2.search(line):
            continue
        cleaned_lines.append(line)
        
    if not ''.join(cleaned_lines).strip():
        cleaned_lines = lines
        
    result = '\n'.join(cleaned_lines)
    result = re.sub(r'\n{3,}', '\n\n', result)
    
    return result.strip()

if __name__ == "__main__":
    sys.stdout.reconfigure(encoding='utf-8')
    
    if len(sys.argv) < 2:
        print("Usage: python chords.py <query>")
        sys.exit(1)
        
    query = " ".join(sys.argv[1:])
    print(f"🔍 Ищем: {query}...")
    
    link, site_type = search_chords(query)
    if not link:
        print("❌ Песня не найдена ни на одном сайте.")
        sys.exit(1)
        
    print(f"🔗 Найдена ссылка ({site_type}): {link}\n")
    print("-" * 40)
    
    chords = get_chords(link, site_type)
    print(chords)
    print("-" * 40)
