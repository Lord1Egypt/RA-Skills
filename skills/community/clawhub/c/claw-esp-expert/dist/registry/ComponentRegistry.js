"use strict";
Object.defineProperty(exports, "__esModule", { value: true });
exports.ComponentRegistry = void 0;
class ComponentRegistry {
    constructor(client, registryBaseUrl = 'https://components.espressif.com') {
        this.client = client || this.createDefaultClient(registryBaseUrl);
        this.registryBaseUrl = registryBaseUrl;
    }
    async resolveComponent(query, target) {
        const normalizedQuery = query.trim();
        if (!normalizedQuery) {
            return {
                status: 'NOT_FOUND',
                query,
                target,
                reason: '查询字符串为空。'
            };
        }
        const response = await this.client.get('/api/components', {
            params: { q: normalizedQuery }
        });
        const components = response.data || [];
        const ranked = this.rankComponents(components, normalizedQuery, target)
            .map((item) => this.toSuggestion(item.component, item.score))
            .slice(0, 5);
        if (ranked.length === 0) {
            return {
                status: 'NOT_FOUND',
                query: normalizedQuery,
                target,
                reason: '官方 Component Registry 中未找到匹配组件。'
            };
        }
        return {
            status: 'OK',
            query: normalizedQuery,
            target,
            suggestion: ranked[0],
            candidates: ranked
        };
    }
    rankComponents(components, query, target) {
        const normalizedQuery = this.normalizeToken(query);
        const targetToken = target ? this.normalizeToken(target) : '';
        return components
            .map((component) => ({
            component,
            score: this.scoreComponent(component, normalizedQuery, targetToken)
        }))
            .filter((item) => item.score > 0)
            .sort((left, right) => right.score - left.score || left.component.name.localeCompare(right.component.name));
    }
    scoreComponent(component, normalizedQuery, targetToken) {
        const namespace = this.normalizeToken(component.namespace);
        const name = this.normalizeToken(component.name);
        const fullName = `${namespace}/${name}`;
        const description = this.normalizeToken(component.latest_version.description || '');
        const targets = (component.latest_version.targets || []).map((item) => this.normalizeToken(item));
        let score = 0;
        if (name === normalizedQuery)
            score += 120;
        if (fullName === normalizedQuery)
            score += 160;
        if (name.includes(normalizedQuery))
            score += 60;
        if (fullName.includes(normalizedQuery))
            score += 50;
        if (description.includes(normalizedQuery))
            score += 15;
        if (namespace === 'espressif')
            score += 80;
        if (component.featured)
            score += 10;
        if (targetToken) {
            if (targets.includes(targetToken)) {
                score += 40;
            }
            else if (targets.length > 0) {
                score -= 20;
            }
        }
        return score;
    }
    toSuggestion(component, score) {
        const latest = component.latest_version;
        const dependency = `${component.namespace}/${component.name}`;
        const version = `^${latest.version}`;
        const idfDependency = latest.dependencies
            ?.find((dependencyItem) => dependencyItem.source === 'idf')
            ?.spec;
        return {
            dependency,
            version,
            component: dependency,
            namespace: component.namespace,
            name: component.name,
            description: latest.description || '暂无描述。',
            documentation: latest.documentation,
            readme: latest.docs?.readme,
            registryUrl: latest.url,
            targets: latest.targets || [],
            idfDependency,
            score,
            addDependencyCommand: `idf.py add-dependency "${dependency}^${latest.version}"`,
            manifestSnippet: [
                'dependencies:',
                `  ${dependency}:`,
                `    version: "${version}"`
            ].join('\n')
        };
    }
    normalizeToken(value) {
        return value.toLowerCase().trim().replace(/[^a-z0-9/_-]+/g, '');
    }
    createDefaultClient(registryBaseUrl) {
        return {
            get: async (requestPath, options) => {
                const url = new URL(requestPath, registryBaseUrl);
                for (const [key, value] of Object.entries(options?.params || {})) {
                    url.searchParams.set(key, value);
                }
                const response = await fetch(url, { method: 'GET' });
                if (!response.ok) {
                    throw new Error(`Component Registry request failed: ${response.status} ${response.statusText}`);
                }
                return {
                    data: await response.json()
                };
            }
        };
    }
}
exports.ComponentRegistry = ComponentRegistry;
//# sourceMappingURL=ComponentRegistry.js.map