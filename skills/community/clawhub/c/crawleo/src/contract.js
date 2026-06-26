export const CRAWLEO_BASE_URL = 'https://api.crawleo.dev';

export const CRAWLEO_ENDPOINTS = Object.freeze({
  search: Object.freeze({
    id: 'search',
    path: '/search',
    method: 'GET',
    requiredQuery: ['query'],
    enumQuery: Object.freeze({ device: ['desktop', 'mobile', 'tablet'] })
  }),
  googleSearch: Object.freeze({
    id: 'google_search',
    path: '/google-search',
    method: 'GET',
    requiredQuery: ['q'],
    enumQuery: Object.freeze({
      tbs: ['qdr:h', 'qdr:d', 'qdr:w', 'qdr:m', 'qdr:y'],
      type: ['search', 'news', 'images', 'places', 'shopping']
    })
  }),
  googleMaps: Object.freeze({
    id: 'google_maps',
    path: '/google-maps',
    method: 'GET',
    requiredQuery: ['q'],
    enumQuery: Object.freeze({})
  }),
  crawl: Object.freeze({
    id: 'crawl',
    path: '/crawl',
    method: 'GET',
    requiredQuery: ['urls'],
    enumQuery: Object.freeze({})
  }),
  headfulBrowser: Object.freeze({
    id: 'headful_browser',
    path: '/headful-browser',
    method: 'GET',
    requiredQuery: ['urls'],
    enumQuery: Object.freeze({ output_format: ['markdown', 'enhanced_html', 'raw_html', 'page_text'] })
  })
});

export const CRAWLEO_ENDPOINTS_BY_PATH = Object.freeze(
  Object.fromEntries(Object.values(CRAWLEO_ENDPOINTS).map((endpoint) => [endpoint.path, endpoint]))
);

export function getEndpointByPath(path) {
  return CRAWLEO_ENDPOINTS_BY_PATH[path];
}
