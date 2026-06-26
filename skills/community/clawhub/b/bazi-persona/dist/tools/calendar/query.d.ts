export interface ChineseCalendarData {
    公历: string;
    农历: string;
    干支日期: string;
    生肖: string;
    纳音: string;
    农历节日?: string;
    公历节日?: string;
    节气: {
        term: string;
        afterDays: number;
        nextTerm?: string;
        beforeNextTermDays?: number;
    };
    二十八宿: string;
    彭祖百忌: string;
    喜神方位: string;
    阳贵神方位: string;
    阴贵神方位: string;
    福神方位: string;
    财神方位: string;
    冲煞: string;
    宜: string;
    忌: string;
}
export interface ParsedDateTimeInput {
    year: number;
    month: number;
    day: number;
    hour: number;
    minute: number;
    second: number;
    display: string;
}
export declare function parseDateTimeInput(input?: string): ParsedDateTimeInput;
export declare function queryChineseCalendar(params: {
    year: number;
    month: number;
    day: number;
}): Promise<ChineseCalendarData | undefined>;
