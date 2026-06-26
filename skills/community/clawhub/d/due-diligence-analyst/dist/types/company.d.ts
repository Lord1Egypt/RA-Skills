/**
 * 公司信息相关类型定义
 */
export interface CompanyBasicInfo {
    name: string;
    legalName?: string;
    registrationNumber?: string;
    foundedDate?: string;
    registeredCapital?: number;
    industry?: string;
    businessScope?: string;
    address?: string;
    status?: 'active' | 'dissolved' | 'suspended';
}
export interface Shareholder {
    name: string;
    type: 'individual' | 'corporate';
    sharePercentage: number;
    investmentAmount?: number;
}
export interface ShareholderStructure {
    shareholders: Shareholder[];
    actualController?: string;
    ultimateBeneficialOwner?: string;
}
export interface RelatedParty {
    name: string;
    relationship: string;
    registrationNumber?: string;
}
export interface HistoricalChange {
    date: string;
    type: 'capital' | 'shareholder' | 'management' | 'address' | 'business_scope' | 'other';
    description: string;
    before?: string;
    after?: string;
}
export interface CompanyProfile {
    basic: CompanyBasicInfo;
    shareholderStructure?: ShareholderStructure;
    relatedParties?: RelatedParty[];
    historicalChanges?: HistoricalChange[];
    collectedAt: string;
}
//# sourceMappingURL=company.d.ts.map