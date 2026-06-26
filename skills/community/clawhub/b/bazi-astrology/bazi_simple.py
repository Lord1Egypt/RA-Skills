import argparse
import collections
from ganzhi import *
from lunar_python import Lunar, Solar
from datas import *
from common import *


class bazi_dayun():
    def __init__(self):
        self.zhus = None
        self.zhis = None
        self.year = 0
        self.month = 0
        self.day = 0
        self.hour = 0
        self.minute = 0
        self.yin = False
        self.female = False
        self.bazi = None
        self.plain_bazi = False
        self.start = None
        self.end = None
        self.runyue = False
        self.me = None

    def get_parser(self, simulated_args=None):
        description = ""
        parser = argparse.ArgumentParser(description=description,
                                         formatter_class=argparse.RawTextHelpFormatter)
        parser.add_argument('year', action="store", help=u'year')
        parser.add_argument('month', action="store", help=u'month')
        parser.add_argument('day', action="store", help=u'day')
        parser.add_argument('hour', action="store", help=u'hour')
        parser.add_argument('minute', action="store", help=u'minute')
        parser.add_argument("--start", help="start year", type=int, default=1850)
        parser.add_argument("--end", help="end year", default='2030')
        # parser.add_argument('-b', action="store_true", default=False, help=u'直接输入八字')
        parser.add_argument('-y', action="store_true", default=False, help=u'是否采用阴历')
        parser.add_argument('-r', action="store_true", default=False, help=u'是否为闰月，仅仅使用于农历')
        parser.add_argument('-n', action="store_true", default=False, help=u'是否为女，默认为男')
        parser.add_argument('--version', action='version',
                            version='%(prog)s 1.0 Rongzhong xu 2022 06 15')
        if simulated_args:
            options = parser.parse_args(simulated_args)
        else:
            options = parser.parse_args()
        self.year = int(options.year)
        self.month = int(options.month)
        self.day = int(options.day)
        # if options.b:
        #     self.hour = options.time
        # else:
        self.hour = int(options.hour)
        self.minute = int(options.minute)
        self.yin = options.y
        self.female = options.n
        self.start = options.start
        self.end = options.end
        self.runyue = options.r

    def get_bazi(self):
        Gans = collections.namedtuple("Gans", "year month day time")
        Zhis = collections.namedtuple("Zhis", "year month day time")

        # if self.plain_bazi:
        #     import sxtwl
        #     gans = Gans(year=self.year[0], month=self.month[0],
        #                 day=self.day[0], time=self.time[0])
        #     zhis = Gans(year=self.year[1], month=self.month[1],
        #                 day=self.day[1], time=self.hour[1])
        #     jds = sxtwl.siZhu2Year(getGZ(self.year), getGZ(self.month), getGZ(self.day), getGZ(self.hour),
        #                            self.start, int(self.end));
        #     for jd in jds:
        #         t = sxtwl.JD2DD(jd)
        #         print("可能出生时间: python bazi.py -g %d %d %d %d :%d:%d" % (t.Y, t.M, t.D, t.h, t.m, round(t.s)))
        #
        # else:
        #
        if not self.yin:
            solar = Solar.fromYmdHms(self.year, self.month, self.day, self.hour, self.minute, 0)
            lunar = solar.getLunar()
        else:
            month_ = self.month * -1 if self.runyue else self.month
            lunar = Lunar.fromYmdHms(self.year, month_, self.day, self.hour, self.minute, 0)

        ba = lunar.getEightChar()
        gans: Gans = Gans(year=ba.getYearGan(), month=ba.getMonthGan(), day=ba.getDayGan(), time=ba.getTimeGan())
        zhis = Zhis(year=ba.getYearZhi(), month=ba.getMonthZhi(), day=ba.getDayZhi(), time=ba.getTimeZhi())
        self.bazi = ba
        self.me = gans.day
        self.zhis = zhis
        self.gans = gans

        alls = list(gans) + list(zhis)
        zhus = [item for item in zip(gans, zhis)]
        self.zhus = zhus
        return alls, zhus

    def check_gan(self, gan, gans):
        result = ''
        if ten_deities[gan]['合'] in gans:
            result += "合" + ten_deities[gan]['合']
        if ten_deities[gan]['冲'] in gans:
            result += "冲" + ten_deities[gan]['冲']
        return result

    def get_shens(self, gan_, zhi_):

        all_shens = []
        for item in year_shens:
            if zhi_ in year_shens[item][self.zhis.year]:
                all_shens.append(item)

        for item in month_shens:
            if gan_ in month_shens[item][self.zhis.month] or zhi_ in month_shens[item][self.zhis.month]:
                all_shens.append(item)

        for item in day_shens:
            if zhi_ in day_shens[item][self.zhis.day]:
                all_shens.append(item)

        for item in g_shens:
            if zhi_ in g_shens[item][self.me]:
                all_shens.append(item)
        return all_shens

    def get_dayun(self, n = 15):
        yun = self.bazi.getYun(not self.female)
        dayuns = []
        Dayun = collections.namedtuple("Dayun", "ganzhi age year shishen_gan shishen_zhi shensha")
        for dayun in yun.getDaYun(n=n)[1:]:
            # 大运干支
            gan_ = dayun.getGanZhi()[0]
            zhi_ = dayun.getGanZhi()[1]
            start_age = dayun.getStartAge()
            start_year = dayun.getStartYear()

            # 大运地支藏干
            dizhicanggan = ''
            for canggan in zhi5[zhi_]:
                # 地支藏干的十神
                dizhicanggan = dizhicanggan + "{}{} ".format(canggan, ten_deities[self.me][canggan])

            # 大运十神
            shishen_gan = "{}{}".format(gan_, ten_deities[self.me][gan_])
            shishen_zhi = dizhicanggan

            # 大运神煞
            shensha = " ".join(self.get_shens(gan_, zhi_))

            this_dayun: Dayun = Dayun(ganzhi=dayun.getGanZhi(), age=start_age, year=start_year,shishen_gan=shishen_gan, shishen_zhi=shishen_zhi,shensha=shensha)
            dayuns.append(this_dayun)

            '''
            #以下这段计算暂不需要
            fu = '*' if (gan_, zhi_) in self.zhus else " "

            

            #下面这一段不知道什么作用
            zhi__ = set()  # 大运地支关系

            for item in self.zhis:

                for type_ in zhi_atts[zhi_]:
                    if item in zhi_atts[zhi_][type_]:
                        zhi__.add(type_ + ":" + item)
            zhi__ = '  '.join(zhi__)

            empty = chr(12288)
            if zhi_ in empties[self.zhus[2]]:
                empty = '空'

            jia = ""
            if gan_ in self.gans:
                for i in range(4):
                    if gan_ == self.gans[i]:
                        if abs(Zhi.index(zhi_) - Zhi.index(self.zhis[i])) == 2:
                            jia = jia + "  --夹：" + Zhi[(Zhi.index(zhi_) + Zhi.index(self.zhis[i])) // 2]
                        if abs(Zhi.index(zhi_) - Zhi.index(self.zhis[i])) == 10:
                            jia = jia + "  --夹：" + Zhi[(Zhi.index(zhi_) + Zhi.index(self.zhis[i])) % 12]

            #输出举例：'2        丁未 冠 天河水    比:丁－合壬　　　　　未－冠 - 己食　丁比　乙枭　　 会:午  六:午  会:巳'
            out = "{1:<4d}{2:<5s}{3} {15} {14} {13}  {4}:{5}{8}{6:{0}<6s}{12}{7}{8}{9} - {10:{0}<10s} {11}".format(
                chr(12288), dayun.getStartAge(), '', dayun.getGanZhi(), ten_deities[self.me][gan_], gan_, self.check_gan(gan_, self.gans),
                zhi_, yinyang(zhi_), ten_deities[self.me][zhi_], zhi5_, zhi__, empty, fu, nayins[(gan_, zhi_)],
                ten_deities[self.me][zhi_])
            gan_index = Gan.index(gan_)
            zhi_index = Zhi.index(zhi_)
            #输出举例：2        丁未 冠 天河水    比:丁－合壬　　　　　未－冠 - 己食　丁比　乙枭　　 会:午  会:巳  六:午  --夹：午  神:寡宿 红艳
            #即：前面的out+ --夹 + 神煞（只有神，没有煞）
            out = out + jia + get_shens(gans, zhis, gan_, zhi_)
            print(out)
            '''
        return dayuns

    def _ganzhi_eq(self, gz_lib, dayun):
        """大运干支是否一致（兼容库返回对象与传入 tuple/str）。"""
        if gz_lib == dayun:
            return True
        a = gz_lib
        b = dayun
        a_str = ''.join(a) if (hasattr(a, '__iter__') and not isinstance(a, str)) else str(a)
        b_str = ''.join(b) if (hasattr(b, '__iter__') and not isinstance(b, str)) else str(b)
        return a_str == b_str

    def get_liunian(self, dayun, n=15):
        """n 与 get_dayun(n) 一致，确保能遍历到所有需要取流年的大运。"""
        yun = self.bazi.getYun(not self.female)
        liunians = []
        Liunian = collections.namedtuple("Liunian", "ganzhi age year shishen_gan shishen_zhi shensha")
        for dayun_ in yun.getDaYun(n=n)[1:]:
            if self._ganzhi_eq(dayun_.getGanZhi(), dayun):
                for liunian in dayun_.getLiuNian():
                    gan2_ = liunian.getGanZhi()[0]
                    zhi2_ = liunian.getGanZhi()[1]
                    liunian_age = liunian.getAge()
                    liunian_year = liunian.getYear()

                    # 流年地支藏干
                    dizhicanggan = ''
                    for canggan in zhi5[zhi2_]:
                        dizhicanggan = dizhicanggan + "{}{} ".format(canggan, ten_deities[self.me][canggan])

                    # 流年十神
                    shishen_gan2 = "{}{}".format(gan2_, ten_deities[self.me][gan2_])
                    shishen_zhi2 = dizhicanggan

                    # 流年神煞
                    shensha2 = " ".join(self.get_shens(gan2_, zhi2_))

                    this_liunian: Liunian = Liunian(ganzhi=liunian.getGanZhi(), age=liunian_age, year=liunian_year,
                                              shishen_gan=shishen_gan2, shishen_zhi=shishen_zhi2, shensha=shensha2)
                    liunians.append(this_liunian)

                    '''
                    #极端地支情况，暂且不考虑
                    all_zhis = set(zhis2) | set(zhi2_)
                    if set('戌亥辰巳').issubset(all_zhis):
                        out = out + "  天罗地网：戌亥辰巳"
                    if set('寅申巳亥').issubset(all_zhis) and len(set('寅申巳亥') & set(zhis)) == 2:
                        out = out + "  四生：寅申巳亥"
                    if set('子午卯酉').issubset(all_zhis) and len(set('子午卯酉') & set(zhis)) == 2:
                        out = out + "  四败：子午卯酉"
                    if set('辰戌丑未').issubset(all_zhis) and len(set('辰戌丑未') & set(zhis)) == 2:
                        out = out + "  四库：辰戌丑未"
                    print(out)
                    '''
                break  # 找到该大运并取完流年后再退出，否则会只处理第一个大运
        return liunians


if __name__ == "__main__":
    simulated_args = ["1992", "08", "09", "11", "50", "-n"]

    ba = bazi_dayun()
    ba.get_parser(simulated_args)
    alls, bazi = ba.get_bazi()
    print(bazi)
    dayuns = ba.get_dayun()
    print(dayuns)
    liunians = ba.get_liunian("丁未")
    print(liunians)